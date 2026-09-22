// Headless-Chrome verification of the seven EN pages at 1366x900 and 375x812:
// motion state, header state, <picture> layout, WebP selection, tap-target
// heights, horizontal overflow, console errors. Full-page screenshots optional.
//   python3 tools/serve.py 8791 src          (no-store server, in another shell)
//   cd tools && npm i puppeteer-core && node verify.js http://localhost:8791 ./shots
// Do NOT verify scroll/animation behaviour in the Claude desktop browser pane:
// it often runs with visibilityState "hidden", where IntersectionObserver,
// scroll events, rAF and lazy images never fire and screenshots come out blank.
const puppeteer = require('puppeteer-core');
const BASE = process.argv[2] || 'http://localhost:8791';
const OUT = process.argv[3] || null;
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PAGES = ['/', '/menu/', '/our-story/', '/after-dark/', '/events/', '/reservation/', '/contact/'];
const VIEWS = [{ w: 1366, h: 900, tag: 'desktop' }, { w: 375, h: 812, tag: 'mobile', mobile: true }];
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  if (OUT) require('fs').mkdirSync(OUT, { recursive: true });
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--autoplay-policy=user-gesture-required', '--hide-scrollbars', '--no-first-run'] });
  const results = [];
  for (const v of VIEWS) for (const path of PAGES) {
    const page = await browser.newPage();
    await page.setViewport({ width: v.w, height: v.h, isMobile: !!v.mobile, hasTouch: !!v.mobile, deviceScaleFactor: 1 });
    const errors = []; page.on('pageerror', e => errors.push(String(e.message))); page.on('console', m => { if (m.type() === 'error' && !/googletagmanager|gtag|HTTP2/.test(m.text())) errors.push(m.text()); });
    await page.goto(BASE + path, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
    await sleep(400);
    const top = await page.evaluate(() => {
      const q = s => document.querySelector(s), qa = s => [...document.querySelectorAll(s)], cs = (e, p) => getComputedStyle(e)[p];
      const h1 = q('.pg-hero__h');
      return {
        motion: document.body.classList.contains('motion'), isScrolled: document.body.classList.contains('is-scrolled'),
        secs: qa('main > section').map(s => (s.classList.contains('is-in') ? 'in' : '--') + ':' + (+cs(s, 'opacity')).toFixed(2)),
        h1Clip: h1 ? cs(h1, 'clipPath') : null, hdrH: Math.round(q('.hdr').getBoundingClientRect().height),
        hScroll: document.documentElement.scrollWidth - innerWidth,
        pictures: qa('main picture').length, pictureDisplay: q('main picture') ? cs(q('main picture'), 'display') : null,
      };
    });
    const total = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < total; y += Math.round(v.h * 0.6)) { await page.evaluate(y => scrollTo(0, y), y); await sleep(120); }
    await sleep(1200);
    const mid = await page.evaluate(() => {
      const q = s => document.querySelector(s), qa = s => [...document.querySelectorAll(s)], cs = (e, p) => getComputedStyle(e)[p];
      const imgs = qa('main > section img').filter(i => !i.closest('.hm-hero') && !i.closest('.pg-hero'));
      const notSettled = imgs.filter(i => cs(i, 'transform') !== 'none' && cs(i, 'transform') !== 'matrix(1, 0, 0, 1, 0, 0)').length;
      const small = qa('a,button').filter(e => innerWidth < 761 && e.getBoundingClientRect().height > 1 && e.getBoundingClientRect().height < 44)
        .map(e => (e.className || e.tagName) + ':' + Math.round(e.getBoundingClientRect().height) + ':' + (e.textContent || '').trim().slice(0, 20));
      return {
        isScrolled: document.body.classList.contains('is-scrolled'), hdrH: Math.round(q('.hdr').getBoundingClientRect().height),
        secs: qa('main > section').map(s => (s.classList.contains('is-in') ? 'in' : '--') + ':' + (+cs(s, 'opacity')).toFixed(2)),
        imgs: imgs.length, imgsNotSettled: notSettled,
        webp: qa('main img').filter(i => i.currentSrc).map(i => /\.webp$/.test(i.currentSrc)).filter(Boolean).length + '/' + qa('main img').filter(i => i.currentSrc).length,
        hScroll: document.documentElement.scrollWidth - innerWidth, smallTargets: small.slice(0, 10),
      };
    });
    await page.evaluate(() => scrollTo(0, 0)); await sleep(500);
    const back = await page.evaluate(() => ({ isScrolled: document.body.classList.contains('is-scrolled'), hdrH: Math.round(document.querySelector('.hdr').getBoundingClientRect().height) }));
    if (OUT) await page.screenshot({ path: `${OUT}/${(path === '/' ? 'home' : path.replace(/\//g, ''))}-${v.tag}.png`, fullPage: true });
    results.push({ path, view: v.tag, top, mid, back, errors: errors.slice(0, 4) });
    await page.close();
  }
  await browser.close();
  for (const r of results) {
    console.log(`\n== ${r.path} @${r.view} ==`);
    console.log(' top :', JSON.stringify({ motion: r.top.motion, scrolled: r.top.isScrolled, hdrH: r.top.hdrH, h1Clip: r.top.h1Clip, hScroll: r.top.hScroll, pictures: r.top.pictures, picDisplay: r.top.pictureDisplay, secs: r.top.secs.join(' ') }));
    console.log(' mid :', JSON.stringify({ scrolled: r.mid.isScrolled, hdrH: r.mid.hdrH, imgs: r.mid.imgs, notSettled: r.mid.imgsNotSettled, webp: r.mid.webp, hScroll: r.mid.hScroll, small: r.mid.smallTargets, secs: r.mid.secs.join(' ') }));
    console.log(' back:', JSON.stringify(r.back), r.errors.length ? ' ERRORS: ' + JSON.stringify(r.errors) : '');
  }
  // Expected: top → hero "in:1.00", others "--:0.00"; mid → all "in:1.00", scrolled:true, hdrH 66, notSettled 0,
  // hScroll 0, small [] (only the sr-only skip link may appear); back → scrolled:false, hdrH 76; no ERRORS.
})().catch(e => { console.error('FATAL', e); process.exit(1); });
