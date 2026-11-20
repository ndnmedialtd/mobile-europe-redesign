// ---- Demo member (mockup login: test / test). Stored in this browser only. ----
window.ME_MEMBER = (function () {
  const KEY = 'me-member';
  const demo = { first: 'Sam', last: 'Taylor', title: 'Head of Network Strategy', company: 'Example Telecom', since: 'March 2025' };
  let mem = null; // fallback if browser storage is blocked
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return mem; } };
  return {
    get: () => read() || (new URLSearchParams(location.search).get('demo') === 'member' ? demo : null),
    login(user, pass) {
      if (String(user).trim().toLowerCase() !== 'test' || pass !== 'test') return false;
      try { localStorage.setItem(KEY, JSON.stringify(demo)); } catch (e) { mem = demo; }
      return true;
    },
    logout() { try { localStorage.removeItem(KEY); } catch (e) {} mem = null; }
  };
})();

// Shared header, footer and mockup toolbar for all pages

// Small pin icon used by pages
window.PIN = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16 3l5 5-3 1-4 4 1 5-2 2-4-4-5 5-1-1 5-5-4-4 2-2 5 1 4-4z"/></svg>';

(function () {
  const page = document.body.dataset.page;      // home | cat | brief | res
  const cat = document.body.dataset.cat || '';
  const IMG = 'https://www.mobileeurope.co.uk/wp-content/uploads/';
  window.ME_IMG = IMG;

  // Category name -> page (5G & Beyond is hand-made; the rest are generated)
  const catHref = c => c === '5G & Beyond' ? 'category-5g.html'
    : 'category-' + c.toLowerCase().replace(/ & /g, '-').replace(/[\/ ]+/g, '-') + '.html';
  window.ME_CAT_HREF = catHref;
  const cats = ['5G & Beyond', 'Access', 'Automation/AI', 'BSS/OSS/CX', 'Cloud/NFV', 'Digital Platforms & APIs', 'Edge', 'Financial/Regulation', 'Optical/IP', 'RAN', 'Satellite', 'Security', 'Sustainability'];

  // On The Briefing and Research pages, the franchise band is the main menu: drop the
  // site's main menu and category menu there (the Next Briefing ticker stays on every page).
  const isBrief = page === 'brief' || page === 'brief-event' || page === 'res';

  // Ticker items: the next Briefing first, then what's coming up
  const tickerItems = [
    `<a href="briefing-event.html"><em>Tue 24 Nov</em> AI in Network Optimisation: Finding Forgotten Revenue · Live online, 09:30 GMT · <u>Register free</u></a>`,
    `<a href="events.html"><em>10 Dec</em> Telecoms in Focus</a>`,
    `<a href="the-briefing.html"><em>4 Feb</em> The Briefing: The critical role of telcos in defence</a>`,
    `<a href="the-briefing.html"><em>15 Apr</em> The Briefing: Extracting the full potential of 5G Standalone</a>`,
    `<a href="research.html"><em>New report</em> OSS: Why trusted data matters as a catalyst for AI modernisation</a>`
  ].join('<i aria-hidden="true">◆</i>');

  const header = `
  ${page === 'brief' || page === 'brief-event' ? `<div class="util"><div class="wrap">
    <a class="tk-label" href="briefing-event.html">Next Briefing</a>
    <div class="ticker" aria-label="Upcoming Briefings and new reports">
      <div class="tk-track">
        <span class="tk-set">${tickerItems}<i aria-hidden="true">◆</i></span>
        <span class="tk-set" aria-hidden="true">${tickerItems}<i aria-hidden="true">◆</i></span>
      </div>
    </div>
    <div class="right"><a href="#">Newsletter</a><a href="#">Advertise</a><a href="#">About</a></div>
  </div></div>` : ''}
  <div class="lb-zone"><div class="wrap"><div class="ad-label">Advertisement</div>
    <a class="gsma-bb" href="white-papers.html" aria-label="Case study by GSMA Industry Services: Looking to deliver a seamless BYOD mobile experience? Download">
      <span class="gs-photo"><img src="https://www.mobileeurope.co.uk/wp-content/uploads/2026/09/GSMA-sept26-wp-696x843.jpg" alt=""></span>
      <span class="gs-copy">
        <span class="gs-kicker">Case Study</span>
        <span class="gs-head">Looking to deliver a seamless BYOD mobile experience?</span>
        <span class="gs-sub">Discover how Cogeco was able to launch its BYOD programme with confidence.</span>
      </span>
      <span class="gs-side">
        <span class="gs-pub"><small>Published by</small><b>GSMA</b><i>Industry Services</i></span>
        <span class="gs-cta"><span class="cta-long">Download the case study</span><span class="cta-short">Download</span></span>
      </span>
    </a>
  </div></div>
  <div class="mast"><div class="wrap">
    <a class="logo logo-img" href="index.html">
      <img src="https://www.mobileeurope.co.uk/wp-content/uploads/2025/08/MobileEurope-logo-wide-strap-v4.png" alt="Mobile Europe: Communications infrastructure and digital services in EMEA" width="1343" height="236">
    </a>
    <div class="franchises">
      <a class="fr brief${page === 'brief' || page === 'brief-event' ? ' active' : ''}" href="the-briefing.html"${page === 'brief' || page === 'brief-event' ? ' aria-current="page"' : ''}><small>Live events</small><b>The Briefing</b><span>Next: 24 Nov · AI &amp; Revenue</span></a>
      <a class="fr res${page === 'res' ? ' active' : ''}" href="research.html"${page === 'res' ? ' aria-current="page"' : ''}><small>Reports</small><b>Independent<br>Research</b><span>New: OSS &amp; AI modernisation</span></a>
    </div>
    <div class="mast-tools">
      <div class="acct-btns">
        <a class="btn subscribe" href="#" data-subscribe>Subscribe</a>
        <a class="btn login" href="#">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6" fill="none" stroke="currentColor" stroke-width="2"/></svg>Log in
        </a>
      </div>
      <small class="acct-note">Log in to register for events, download reports and white papers, and manage your subscription.</small>
    </div>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mmenu"><span></span><span></span><span></span></button>
  </div></div>
  ${isBrief ? '' : `<div class="nav"><div class="wrap">
    <a class="nav-me" href="index.html" aria-label="Mobile Europe home" tabindex="-1">ME</a>
    <button class="nav-search" id="search-toggle" aria-label="Search" aria-expanded="false" aria-controls="search-panel">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
    </button>
    <a href="index.html" class="${page === 'home' ? 'on' : ''}">Home</a>
    <a href="news.html" class="${page === 'news' ? 'on' : ''}">News</a><a href="insights.html" class="${page === 'insights' ? 'on' : ''}">Insights</a><a href="cxo.html" class="${page === 'cxo' ? 'on' : ''}">CxO Zone</a><a href="white-papers.html" class="${page === 'white-papers' ? 'on' : ''}">White Paper Hub</a><a href="videos.html" class="${page === 'videos' ? 'on' : ''}">Videos</a><a href="events.html" class="${page === 'events' ? 'on' : ''}">Events</a>
    <div class="nav-promo" aria-roledescription="carousel" aria-label="Next Briefing and latest report">
      <div class="np-slides">
        <a class="np-slide cur" href="briefing-event.html"><b>Next Briefing</b><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg><span>AI &amp; Revenue</span><u>24 November</u></a>
        <a class="np-slide" href="research.html" tabindex="-1" aria-hidden="true"><b>New report</b><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h9l4 4v14H6z M14 3v5h5" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg><span>OSS &amp; AI modernisation</span><u>Download</u></a>
      </div>
      <button class="np-next" type="button" aria-label="Show next: latest report"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    </div>
  </div></div>
  <div class="search-panel" id="search-panel" hidden><div class="wrap">
    <form role="search" onsubmit="return false">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <input placeholder="Search news, insights, reports and Briefings…" aria-label="Search Mobile Europe">
      <button class="btn" type="submit">Search</button>
    </form>
  </div></div>
  <div class="cats"><div class="wrap">
    ${cats.map(c => `<a href="${catHref(c)}" class="${c === cat ? 'on' : ''}">${c.replace('&', '&amp;')}</a>`).join('')}
  </div></div>`}`;

  const footer = `
  <footer class="site"><div class="wrap">
    <div class="cols">
      <div>
        <a class="foot-logo" href="index.html"><img src="https://www.mobileeurope.co.uk/wp-content/uploads/2025/08/MobileEurope-logo-wide-strap-white-v1.png" alt="Mobile Europe: Communications infrastructure and digital services in EMEA" width="1000" height="176"></a>
        <p style="margin-top:12px;max-width:300px">Covering communications infrastructure and digital services in EMEA.</p>
      </div>
      <div><h5>Editorial</h5><a href="news.html">News</a><a href="insights.html">Insights</a><a href="cxo.html">CxO Zone</a><a href="white-papers.html">White Paper Hub</a><a href="videos.html">Videos</a></div>
      <div><h5>Franchises</h5><a href="the-briefing.html">The Briefing</a><a href="research.html">Independent Research</a><a href="#">Telecoms in Focus</a><a href="events.html">Events</a></div>
      <div><h5>Company</h5><a href="#">About</a><a href="#">Advertise</a><a href="#">Editorial Advisory Board</a><a href="#">Contact</a><a href="#">Privacy</a></div>
    </div>
    <div class="legal">Design mockup: not the live site. Content and images from mobileeurope.co.uk, used for layout only.</div>
  </div></footer>`;

  const pages = [['index.html', 'home', 'Homepage'], ['news.html', 'news', 'News'], ['insights.html', 'insights', 'Insights'], ['cxo.html', 'cxo', 'CxO Zone'], ['white-papers.html', 'white-papers', 'White Paper Hub'], ['videos.html', 'videos', 'Videos'], ['events.html', 'events', 'Events'], ['category-5g.html', 'cat', '5G & Beyond'], ['article.html', 'article', 'Article'], ['the-briefing.html', 'brief', 'The Briefing'], ['briefing-event.html', 'brief-event', 'Briefing sign-up'], ['research.html', 'res', 'Research'], ['members.html', 'members', 'Members area']];
  const idx = Math.max(0, pages.findIndex(p => p[1] === page));
  const toolbar = `<div class="mock">
    <span class="lbl" style="padding:0 2px 0 6px;color:#888">Mockup</span><select id="ver-switch" aria-label="Mockup version"><option value="me-redesign-d2a">D2A</option><option value="me-redesign-d2b">D2B</option><option value="me-redesign-d2c">D2C</option><option value="me-redesign-d2d">D2D</option><option value="me-redesign-d2e">D2E</option><option value="me-redesign-d2g">D2G</option></select><span class="div"></span>
    <a href="${pages[(idx + pages.length - 1) % pages.length][0]}" aria-label="Previous page">←</a>
    <select aria-label="Jump to page" onchange="location.href=this.value">
      ${pages.map(p => `<option value="${p[0]}"${p[1] === page ? ' selected' : ''}>${p[2]}</option>`).join('')}
    </select>
    <a href="${pages[(idx + 1) % pages.length][0]}" aria-label="Next page">→</a>
  </div>`;

  document.getElementById('site-header').outerHTML = header;
  // The duplicate ticker copy is only there for the seamless loop: keep it out of keyboard focus
  document.querySelectorAll('.tk-set[aria-hidden] a').forEach(l => { l.tabIndex = -1; });
  const pinModal = `
  <div class="modal" id="pin-modal" role="dialog" aria-modal="true" aria-labelledby="pin-title" hidden>
    <div class="modal-box">
      <button class="modal-x" data-close aria-label="Close">×</button>
      <div class="pin-inline" style="margin-bottom:8px">${window.PIN || ''} Pinned posts</div>
      <h3 id="pin-title">Pin your post on Mobile Europe</h3>
      <p>Hold your content at the top of News or Insights, clearly labelled as sponsored. Tell us a little about your campaign and our sales team will be in touch.</p>
      <form id="pin-form">
        <div class="two"><input required placeholder="Name*"><input required placeholder="Company*"></div>
        <div class="two"><input required type="email" placeholder="Business email*"><input placeholder="Phone"></div>
        <select><option>Where would you like to pin?</option><option>News</option><option>Insights</option><option>Both</option><option>Not sure yet</option></select>
        <select><option>Preferred timing</option><option>Within 2 weeks</option><option>This month</option><option>Next quarter</option></select>
        <textarea rows="3" placeholder="What would you like to promote?"></textarea>
        <button class="btn red" type="submit">Send to our sales team</button>
        <small>Mockup only: this form doesn’t send anything yet.</small>
      </form>
      <div class="thanks-msg" hidden><h3>Thanks, we’ll be in touch</h3><p>Someone from the Mobile Europe sales team will contact you shortly to discuss pinned post options.</p><button class="btn" data-close>Close</button></div>
    </div>
  </div>`;

  const loginModal = `
  <div class="modal" id="login-modal" role="dialog" aria-modal="true" aria-labelledby="login-title" hidden>
    <div class="modal-box login-box">
      <button class="modal-x" data-close aria-label="Close">×</button>
      <img class="login-logo" src="https://www.mobileeurope.co.uk/wp-content/uploads/2025/08/MobileEurope-logo-wide-strap-v4.png" alt="Mobile Europe">
      <h3 id="login-title">Log in to Mobile Europe</h3>
      <ul class="perks">
        <li>Register for <b>The Briefing</b> live events in one click</li>
        <li>Download <b>Independent Research</b> reports and white papers</li>
        <li>Manage your newsletters and subscription</li>
        <li>Choose the <b>topics</b> you most want to read</li>
      </ul>
      <form id="login-form">
        <label>Email or username<input required type="text" name="user" autocomplete="username" placeholder="you@company.com"></label>
        <label>Password<input required type="password" name="pass" autocomplete="current-password" placeholder="••••••••"></label>
        <p class="login-err" role="alert" hidden>Those details didn’t match. In this mockup, use <b>test</b> / <b>test</b>.</p>
        <div class="login-row"><label class="chk"><input type="checkbox"> Keep me logged in</label><a href="#">Forgot password?</a></div>
        <button class="btn subscribe" type="submit">Log in</button>
        <small>Mockup: log in with <b>test</b> / <b>test</b> to see the Members area.</small>
      </form>
      <div class="thanks-msg" hidden><h3>You’re logged in</h3><p>In the live site you’d now see your saved events, downloads and subscription settings.</p><button class="btn" data-close>Close</button></div>
      <div class="login-foot">New to Mobile Europe? <a href="#">Create a free account →</a></div>
    </div>
  </div>`;

  const subscribeModal = `
  <div class="modal" id="subscribe-modal" role="dialog" aria-modal="true" aria-labelledby="sub-title" hidden>
    <div class="modal-box login-box">
      <button class="modal-x" data-close aria-label="Close">×</button>
      <img class="login-logo" src="https://www.mobileeurope.co.uk/wp-content/uploads/2025/08/MobileEurope-logo-wide-strap-v4.png" alt="Mobile Europe">
      <h3 id="sub-title">Subscribe</h3>
      <p class="sub-intro">Get the essential EMEA telecoms news and analysis in your inbox, free.</p>
      <form id="subscribe-form">
        <div class="two"><input required placeholder="First name*" autocomplete="given-name"><input required placeholder="Last name*" autocomplete="family-name"></div>
        <input required type="email" placeholder="Business email*" autocomplete="email">
        <div class="two"><input placeholder="Job title" autocomplete="organization-title"><input placeholder="Company" autocomplete="organization"></div>
        <label class="acct-opt"><input type="checkbox" id="sub-account" checked> <span><b>Also register for a free Mobile Europe account</b></span></label>
        <div class="acct-extra" id="sub-extra">
          <ul class="perks">
            <li>Register for <b>The Briefing</b> live events in one click</li>
            <li>Download <b>Independent Research</b> reports and white papers</li>
            <li>Manage your newsletters and subscription</li>
        <li>Choose the <b>topics</b> you most want to read</li>
          </ul>
          <input type="password" placeholder="Create a password" autocomplete="new-password" aria-label="Create a password">
        </div>
        <button class="btn red" type="submit">Subscribe</button>
        <small>Mockup only: this form doesn’t send anything yet. You can unsubscribe at any time.</small>
      </form>
      <div class="thanks-msg" hidden><h3>You’re subscribed</h3><p>Look out for your first newsletter. If you created an account, you can now register for Briefings and download reports in one click.</p><button class="btn" data-close>Close</button></div>
      <div class="login-foot">Already have an account? <a href="#" data-login>Log in →</a></div>
    </div>
  </div>`;

  document.getElementById('site-footer').outerHTML = footer + toolbar + pinModal + loginModal + subscribeModal;

  // Pop-ups: "Pin your post" (sales) and "Log in"
  let lastFocus = null;
  function openModal(id) {
    const m = document.getElementById(id);
    lastFocus = document.activeElement;
    m.hidden = false;
    m.querySelector('form').hidden = false;
    m.querySelector('.thanks-msg').hidden = true;
    document.body.classList.add('modal-open');
    m.querySelector('input').focus();
  }
  function closeModals() {
    if (!document.querySelector('.modal:not([hidden])')) return;
    document.querySelectorAll('.modal').forEach(m => { m.hidden = true; });
    document.body.classList.remove('modal-open');
    if (lastFocus) lastFocus.focus();
  }
  document.addEventListener('click', e => {
    if (e.target.closest('[data-pin-cta]')) { e.preventDefault(); openModal('pin-modal'); }
    else if (e.target.closest('[data-subscribe], .nl .btn, .art-nl .btn')) { e.preventDefault(); closeModals(); openModal('subscribe-modal'); }
    else if (e.target.closest('.login, [data-login]')) { e.preventDefault(); closeModals(); if (window.ME_MEMBER && ME_MEMBER.get()) location.href = 'members.html'; else openModal('login-modal'); }
    else if (e.target.closest('[data-close]') || e.target.classList.contains('modal')) closeModals();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModals(); });
  const acct = document.getElementById('sub-account');
  acct.addEventListener('change', () => { document.getElementById('sub-extra').hidden = !acct.checked; });
  document.querySelectorAll('.modal form:not(#login-form)').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault(); f.hidden = true; f.closest('.modal-box').querySelector('.thanks-msg').hidden = false;
  }));

  // Countdown to next Briefing (24 Nov 2026 09:30 GMT)
  const target = Date.UTC(2026, 10, 24, 9, 30);
  function tick() {
    let s = Math.max(0, Math.floor((target - Date.now()) / 1000));
    const d = Math.floor(s / 86400); s %= 86400;
    const h = Math.floor(s / 3600); s %= 3600;
    const m = Math.floor(s / 60);
    document.querySelectorAll('[data-cd]').forEach(el => {
      el.innerHTML = [[d, 'Days'], [h, 'Hrs'], [m, 'Min']].map(([v, l]) => `<div><b>${String(v).padStart(2, '0')}</b><small>${l}</small></div>`).join('');
    });
  }
  tick(); setInterval(tick, 30000);
})();

// Add pin icons to elements marked data-pin
document.querySelectorAll('[data-pin]').forEach(el => el.insertAdjacentHTML('afterbegin', window.PIN));

// Sponsored pinned posts: drop each one into a random middle position
// of its grid (never first, never last) on every page load.
document.querySelectorAll('.pin-slot:not([data-fixed])').forEach(slot => {
  const grid = slot.parentElement;
  const others = [...grid.children].filter(el => el !== slot);
  if (others.length < 3) return;
  const pos = 1 + Math.floor(Math.random() * (others.length - 1)); // 1 .. n-1
  grid.insertBefore(slot, others[pos]);
});

// Search: magnifying glass in the menu opens a search bar under the nav
(function () {
  const btn = document.getElementById('search-toggle');
  const panel = document.getElementById('search-panel');
  if (!btn || !panel) return;
  btn.addEventListener('click', () => {
    const open = panel.hidden;
    panel.hidden = !open;
    btn.setAttribute('aria-expanded', String(open));
    btn.classList.toggle('on', open);
    if (open) panel.querySelector('input').focus();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !panel.hidden) { panel.hidden = true; btn.classList.remove('on'); btn.setAttribute('aria-expanded', 'false'); btn.focus(); }
  });
})();

// Back to top: red circle with an arrow, shown after scrolling down
(function () {
  const b = document.createElement('button');
  b.className = 'to-top';
  b.type = 'button';
  b.setAttribute('aria-label', 'Back to top');
  b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  document.body.appendChild(b);
  const toggle = () => b.classList.toggle('show', window.scrollY > 600);
  window.addEventListener('scroll', toggle, { passive: true });
  toggle();
  b.addEventListener('click', () => {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });
})();


// Main-menu promo carousel: Next Briefing <-> latest report (arrow, plus gentle auto-advance).
// On narrower screens the same promo appears as a strip under the main menu and category bar.
(function () {
  const original = document.querySelector('.nav .nav-promo');
  if (!original) return;
  const cats = document.querySelector('.cats');
  if (cats) {
    const strip = document.createElement('div');
    strip.className = 'promo-strip';
    const wrap = document.createElement('div');
    wrap.className = 'wrap';
    wrap.appendChild(original.cloneNode(true));
    strip.appendChild(wrap);
    cats.after(strip);
  }
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const labels = ['Show next: latest report', 'Show next: next Briefing'];
  document.querySelectorAll('.nav-promo').forEach(box => {
    const slides = [...box.querySelectorAll('.np-slide')];
    const btn = box.querySelector('.np-next');
    let i = 0, timer = null;
    function go(n) {
      slides[i].classList.remove('cur'); slides[i].setAttribute('aria-hidden', 'true'); slides[i].tabIndex = -1;
      i = (n + slides.length) % slides.length;
      slides[i].classList.add('cur'); slides[i].removeAttribute('aria-hidden'); slides[i].removeAttribute('tabindex');
      btn.setAttribute('aria-label', labels[i]);
    }
    function restart() { if (reduce) return; clearInterval(timer); timer = setInterval(() => go(i + 1), 7000); }
    btn.addEventListener('click', () => { go(i + 1); restart(); });
    box.addEventListener('mouseenter', () => clearInterval(timer));
    box.addEventListener('mouseleave', restart);
    box.addEventListener('focusin', () => clearInterval(timer));
    restart();
  });
})();

// Swipeable carousel (White Paper Hub pinned white papers): native swipe/scroll + arrows + dots
document.querySelectorAll('.wp-carousel').forEach(c => {
  const track = c.querySelector('.wpc-track');
  const slides = [...track.children];
  const dots = [...c.querySelectorAll('.wpc-dots button')];
  const idx = () => Math.round(track.scrollLeft / track.clientWidth);
  const goTo = n => track.scrollTo({ left: Math.max(0, Math.min(n, slides.length - 1)) * track.clientWidth, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  const update = () => {
    const i = idx();
    dots.forEach((d, k) => d.setAttribute('aria-current', k === i ? 'true' : 'false'));
    c.querySelector('.prev').disabled = i === 0;
    c.querySelector('.next').disabled = i === slides.length - 1;
  };
  c.querySelector('.prev').addEventListener('click', () => goTo(idx() - 1));
  c.querySelector('.next').addEventListener('click', () => goTo(idx() + 1));
  dots.forEach((d, k) => d.addEventListener('click', () => goTo(k)));
  track.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { e.preventDefault(); goTo(idx() + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(idx() - 1); }
  });
  let t; track.addEventListener('scroll', () => { clearTimeout(t); t = setTimeout(update, 60); }, { passive: true });
  update();
});


// Telecoms in Focus banner: respect reduced-motion (show the still poster instead of the moving video)
(function () {
  const v = document.querySelector('.tif-bg');
  if (v && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { v.removeAttribute('autoplay'); v.pause(); }
})();

// MPUs: fill every 300×250 slot with real creatives, alternating ENEA (image) and the video ad
(function () {
  const ENEA = 'https://tpc.googlesyndication.com/simgad/12284539410342202964';
  const VIDEO = 'https://s0.2mdn.net/dfp/260406/19415646/1794400797422/video.mp4';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.ad.ad-mpu').forEach((slot, n) => {
    const a = document.createElement('a');
    a.className = 'mpu-creative';
    a.href = '#';
    a.rel = 'sponsored';
    if (n % 2 === 0) {
      a.href = 'white-papers.html';
      a.setAttribute('aria-label', 'Advertisement: ENEA, Detecting and countering fraud and revenue leakage in mobile networks');
      a.innerHTML = `<img src="${ENEA}" width="300" height="250" alt="ENEA: Detecting and Countering Fraud and Revenue Leakage in Mobile Networks">`;
    } else {
      a.setAttribute('aria-label', 'Advertisement (video)');
      a.innerHTML = `<video src="${VIDEO}" width="300" height="250" muted loop playsinline ${reduce ? '' : 'autoplay'} preload="metadata" aria-hidden="true"></video>`;
    }
    slot.replaceWith(a);
  });
})();

// Slide-in menu (opened from the ☰ button on phones and small tablets)
(function () {
  const page = document.body.dataset.page;
  const cat = document.body.dataset.cat || '';
  const catHref = window.ME_CAT_HREF || (() => '#');
  const cats = ['5G & Beyond', 'Access', 'Automation/AI', 'BSS/OSS/CX', 'Cloud/NFV', 'Digital Platforms & APIs', 'Edge', 'Financial/Regulation', 'Optical/IP', 'RAN', 'Satellite', 'Security', 'Sustainability'];
  const sections = [['index.html', 'home', 'Home'], ['news.html', 'news', 'News'], ['insights.html', 'insights', 'Insights'], ['cxo.html', 'cxo', 'CxO Zone'], ['white-papers.html', 'white-papers', 'White Paper Hub'], ['videos.html', 'videos', 'Videos'], ['events.html', 'events', 'Events']];
  const esc = t => t.replace(/&/g, '&amp;');
  const panel = document.createElement('div');
  panel.className = 'mmenu';
  panel.id = 'mmenu';
  panel.hidden = true;
  panel.innerHTML = `
    <div class="mm-backdrop" data-mm-close></div>
    <nav class="mm-panel" role="dialog" aria-modal="true" aria-label="Menu">
      <div class="mm-head">
        <a href="index.html" class="mm-logo"><img src="https://www.mobileeurope.co.uk/wp-content/uploads/2025/08/MobileEurope-logo-wide-strap-v4.png" alt="Mobile Europe home"></a>
        <button class="mm-close" type="button" data-mm-close aria-label="Close menu">×</button>
      </div>
      <form class="mm-search" role="search" onsubmit="return false">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        <input placeholder="Search Mobile Europe" aria-label="Search Mobile Europe">
      </form>
      <div class="mm-acct">
        <a class="btn subscribe" href="#" data-subscribe>Subscribe</a>
        <a class="btn login" href="#" data-login>Log in</a>
      </div>
      <ul class="mm-sections">
        ${sections.map(([h, k, t]) => `<li><a href="${h}"${k === page ? ' aria-current="page"' : ''}>${t}<span aria-hidden="true">›</span></a></li>`).join('')}
      </ul>
      <div class="mm-fr">
        <a class="mm-brief" href="the-briefing.html"${page === 'brief' || page === 'brief-event' ? ' aria-current="page"' : ''}><b>The Briefing</b><span>Next: 24 Nov · AI &amp; Revenue</span></a>
        <a class="mm-res" href="research.html"${page === 'res' ? ' aria-current="page"' : ''}><b>Independent Research</b><span>New: OSS &amp; AI modernisation</span></a>
      </div>
      <div class="mm-label">Topics</div>
      <div class="mm-topics">
        ${cats.map(c => `<a href="${catHref(c)}"${c === cat ? ' aria-current="page"' : ''}>${esc(c)}</a>`).join('')}
      </div>
      <a class="mm-next" href="briefing-event.html">
        <small>Next Briefing · Tue 24 Nov</small>
        <b>AI in Network Optimisation: Finding Forgotten Revenue</b>
        <span class="btn pink">Register free</span>
      </a>
      <div class="mm-foot"><a href="#">Newsletter</a><a href="#">Advertise</a><a href="#">About</a><a href="#">Contact</a></div>
    </nav>`;
  document.body.appendChild(panel);

  const burger = document.querySelector('.burger');
  if (!burger) return;
  let last = null;
  function open() {
    last = document.activeElement;
    panel.hidden = false;
    requestAnimationFrame(() => panel.classList.add('open'));
    document.body.classList.add('modal-open');
    burger.setAttribute('aria-expanded', 'true');
    panel.querySelector('.mm-close').focus();
  }
  function close() {
    if (panel.hidden) return;
    panel.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('modal-open');
    setTimeout(() => { panel.hidden = true; }, 250);
    if (last) last.focus();
  }
  burger.addEventListener('click', open);
  panel.addEventListener('click', e => {
    if (e.target.closest('[data-mm-close]')) close();
    else if (e.target.closest('[data-subscribe], [data-login]')) close(); // the pop-up takes over
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') close();
    // keep keyboard focus inside the open menu
    if (e.key === 'Tab' && !panel.hidden) {
      const f = [...panel.querySelectorAll('a, button, input')];
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });
})();

// Sticky main menu: show the small ME mark once the bar is stuck to the top
(function () {
  const nav = document.querySelector('.nav');
  if (!nav) return;
  const me = nav.querySelector('.nav-me');
  const sentinel = document.createElement('div');
  sentinel.setAttribute('aria-hidden', 'true');
  sentinel.style.cssText = 'height:1px;margin-bottom:-1px';
  nav.before(sentinel);
  new IntersectionObserver(([e]) => {
    const stuck = !e.isIntersecting && e.boundingClientRect.top < 0;
    nav.classList.toggle('stuck', stuck);
    if (me) me.tabIndex = stuck ? 0 : -1;
  }).observe(sentinel);
})();


// Mockup only: switch between header versions (remembered while browsing; ?header=tabs|split|current also works)
(function () {
  const sel = document.getElementById('hdr-var');
  const fromUrl = new URLSearchParams(location.search).get('header');
  let v = fromUrl;
  if (!v) { try { v = localStorage.getItem('me-header2'); } catch (e) {} }
  if (!['current', 'tabs', 'split'].includes(v)) v = 'tabs';   // folder tabs are now the default
  const apply = val => {
    document.body.classList.remove('hdr-tabs', 'hdr-split');
    if (val !== 'current') document.body.classList.add('hdr-' + val);
    try { localStorage.setItem('me-header2', val); } catch (e) {}
  };
  apply(v);
  if (sel) { sel.value = v; sel.addEventListener('change', () => apply(sel.value)); }
})();

// Listing pages: group the section title and its intro so the intro can sit beside the title on wide screens
document.querySelectorAll('h1.ptitle').forEach(h => {
  const p = h.nextElementSibling;
  if (!p || !p.classList.contains('pdesc')) return;
  const wrap = document.createElement('div');
  wrap.className = 'page-head';
  h.before(wrap);
  wrap.append(h, p);
});

// Briefing list: "SECURITY | IN 25 DAYS" — days until each event, worked out from today's date
(function () {
  const today = new Date(); today.setHours(0, 0, 0, 0);
  document.querySelectorAll('.loz[data-date]').forEach(l => {
    const [y, m, d] = l.dataset.date.split('-').map(Number);
    const days = Math.round((new Date(y, m - 1, d) - today) / 86400000);
    const topic = l.querySelector('.topic');
    if (!topic || days < 0) return;
    const label = days === 0 ? 'Today' : days === 1 ? 'Tomorrow' : `In ${days} days`;
    topic.insertAdjacentHTML('beforeend', `<span class="loz-days"> | ${label}</span>`);
  });
})();


// Login form: test / test logs in and opens the Members area
(function () {
  const form = document.getElementById('login-form');
  if (!form) return;
  form.addEventListener('submit', e => {
    e.preventDefault();
    const ok = ME_MEMBER.login(form.user.value, form.pass.value);
    form.querySelector('.login-err').hidden = ok;
    if (ok) {
      let url = 'members.html';
      try { localStorage.getItem('me-member') || (url += '?demo=member'); } catch (err) { url += '?demo=member'; }
      location.href = url;
    } else {
      form.pass.value = ''; form.pass.focus();
    }
  });
})();

// Logged-in header: the Log in buttons become "Hi, Sam" and go to the Members area
(function () {
  const m = ME_MEMBER.get();
  if (!m) return;
  document.querySelectorAll('.login').forEach(b => {
    b.innerHTML = `<span class="av">${m.first[0]}${m.last[0]}</span><span class="nm">${m.first}</span>`;
    b.title = `${m.first} ${m.last}: your Members area`;
    b.setAttribute('href', 'members.html');
    b.setAttribute('aria-label', 'Your Members area');
  });
  const note = document.querySelector('.acct-note');
  if (note) note.innerHTML = `Welcome back, ${m.first}. <a href="members.html">View your downloads, events and topics</a>.`;
})();


// ===== D2C: "three sites in one" header =====
(function () {
  const page = document.body.dataset.page;
  const site = page === 'brief' || page === 'brief-event' ? 'brief' : page === 'res' ? 'res' : 'me';
  const ME_NAV = [['index.html', 'Home'], ['news.html', 'News'], ['insights.html', 'Insights'], ['cxo.html', 'CxO Zone'], ['white-papers.html', 'White Papers'], ['videos.html', 'Videos'], ['events.html', 'Events']];
  const BRIEF_NAV = [['the-briefing.html', 'Upcoming Briefings'], ['#', 'On demand'], ['#', 'Sponsor a Briefing'], ['#', 'Contact']];
  const RES_NAV = [['research.html', 'All reports'], ['research.html#analysts', 'Our analysts'], ['#', 'Topics'], ['#', 'Commission research']];
  const ME_ON = { home: 'index.html', news: 'news.html', cat: 'news.html', article: 'news.html', insights: 'insights.html', cxo: 'cxo.html', 'white-papers': 'white-papers.html', videos: 'videos.html', events: 'events.html' };
  const [items, on] = { me: [ME_NAV, ME_ON[page]], brief: [BRIEF_NAV, 'the-briefing.html'], res: [RES_NAV, 'research.html'] }[site];
  const nav = items.map(([h, t]) => `<a href="${h}"${h === on ? ' class="on" aria-current="page"' : ''}>${t}</a>`).join('');
  const tab = s => s === site ? ' on" aria-current="true' : '';
  const hasSearch = !!document.getElementById('search-toggle');
  const html = `<header class="tri" data-site="${site}">
    <div class="wrap tri-tabs">
      <a class="tri-tab me${tab('me')}" href="index.html" aria-label="Mobile Europe home">
        <img class="tri-logo" src="../brand/mobile-europe-logo-strap.png" alt="Mobile Europe: Communications infrastructure and digital services in EMEA" width="1343" height="236">
        <img class="tri-mark" src="../brand/me-mark.png" alt="" width="400" height="400">
      </a>
      <a class="tri-tab brief${tab('brief')}" href="the-briefing.html"><b>The Briefing</b></a>
      <a class="tri-tab res${tab('res')}" href="research.html"><b>Independent Research</b></a>
    </div>
    <div class="tri-bar"><div class="wrap">
      <nav class="tri-nav" aria-label="Site menu">${nav}</nav>
      <div class="tri-tools">
        ${hasSearch ? '<button class="tri-ico" type="button" id="tri-search" aria-label="Search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg></button>' : ''}
        <a class="tri-sub" href="#" data-subscribe>Subscribe</a>
        <a class="tri-login" href="#" data-login>Log in</a>
        <button class="tri-ico tri-menu" type="button" id="tri-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
      </div>
    </div></div>
  </header>`;
  const anchor = document.querySelector('.lb-zone') || document.querySelector('.mast');
  if (!anchor) return;
  anchor.insertAdjacentHTML('afterend', html);
  const s = document.getElementById('tri-search');
  if (s) s.addEventListener('click', () => document.getElementById('search-toggle').click());
  document.getElementById('tri-menu').addEventListener('click', () => { const b = document.querySelector('.burger'); if (b) b.click(); });
  const m = window.ME_MEMBER && ME_MEMBER.get();
  if (m) { const l = document.querySelector('.tri-login'); l.textContent = 'Hi, ' + m.first; l.setAttribute('href', 'members.html'); l.removeAttribute('data-login'); }
})();

// Version 1 / D2C switch (mockup only): same page, other version
(function () {
  const sel = document.getElementById('ver-switch'); if (!sel) return;
  const here = (location.pathname.match(/\/(me-redesign(?:-d2[a-g])?)\//) || [])[1] || 'me-redesign';
  sel.value = here;
  // pages that only exist in D2A/D2B fall back to the homepage elsewhere
  const ONLY_NEW = ['about.html', 'editorial-board.html', 'white-paper.html'];
  sel.addEventListener('change', () => {
    let file = location.pathname.split('/').pop() || 'index.html';
    if (/^me-redesign(-d2c)?$/.test(sel.value) && ONLY_NEW.includes(file)) file = 'index.html';
    location.href = '../' + sel.value + '/' + file + location.search + location.hash;
  });
})();
