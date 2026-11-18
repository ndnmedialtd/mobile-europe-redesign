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
  <div class="util"><div class="wrap">
    <a class="tk-label" href="briefing-event.html">Next Briefing</a>
    <div class="ticker" aria-label="Upcoming Briefings and new reports">
      <div class="tk-track">
        <span class="tk-set">${tickerItems}<i aria-hidden="true">◆</i></span>
        <span class="tk-set" aria-hidden="true">${tickerItems}<i aria-hidden="true">◆</i></span>
      </div>
    </div>
    <div class="right"><a href="#">Newsletter</a><a href="#">Advertise</a><a href="#">About</a></div>
  </div></div>
  <div class="lb-zone"><div class="wrap"><div class="ad-label">Advertisement</div><div class="ad ad-lb-full">Full-width leaderboard<small>1200×150 (responsive) · GAM · 320×100 on mobile</small></div></div></div>
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
    <button class="burger" aria-label="Menu">☰</button>
  </div></div>
  ${isBrief ? '' : `<div class="nav"><div class="wrap">
    <button class="nav-search" id="search-toggle" aria-label="Search" aria-expanded="false" aria-controls="search-panel">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
    </button>
    <a href="index.html" class="${page === 'home' ? 'on' : ''}">Home</a>
    <a href="news.html" class="${page === 'news' ? 'on' : ''}">News</a><a href="insights.html" class="${page === 'insights' ? 'on' : ''}">Insights</a><a href="cxo.html" class="${page === 'cxo' ? 'on' : ''}">CxO Zone</a><a href="white-papers.html" class="${page === 'white-papers' ? 'on' : ''}">White Paper Hub</a><a href="videos.html" class="${page === 'videos' ? 'on' : ''}">Videos</a><a href="events.html" class="${page === 'events' ? 'on' : ''}">Events</a>
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

  const pages = [['index.html', 'home', 'Homepage'], ['news.html', 'news', 'News'], ['insights.html', 'insights', 'Insights'], ['cxo.html', 'cxo', 'CxO Zone'], ['white-papers.html', 'white-papers', 'White Paper Hub'], ['videos.html', 'videos', 'Videos'], ['events.html', 'events', 'Events'], ['category-5g.html', 'cat', '5G & Beyond'], ['article.html', 'article', 'Article'], ['the-briefing.html', 'brief', 'The Briefing'], ['briefing-event.html', 'brief-event', 'Briefing sign-up'], ['research.html', 'res', 'Research']];
  const idx = Math.max(0, pages.findIndex(p => p[1] === page));
  const toolbar = `<div class="mock">
    <span class="lbl" style="padding:0 6px;color:#888">Mockup</span>
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
      </ul>
      <form id="login-form">
        <label>Business email<input required type="email" autocomplete="username" placeholder="you@company.com"></label>
        <label>Password<input required type="password" autocomplete="current-password" placeholder="••••••••"></label>
        <div class="login-row"><label class="chk"><input type="checkbox"> Keep me logged in</label><a href="#">Forgot password?</a></div>
        <button class="btn subscribe" type="submit">Log in</button>
        <small>Mockup only: this form doesn’t log you in yet.</small>
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
    else if (e.target.closest('.login, [data-login]')) { e.preventDefault(); closeModals(); openModal('login-modal'); }
    else if (e.target.closest('[data-close]') || e.target.classList.contains('modal')) closeModals();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModals(); });
  const acct = document.getElementById('sub-account');
  acct.addEventListener('change', () => { document.getElementById('sub-extra').hidden = !acct.checked; });
  document.querySelectorAll('.modal form').forEach(f => f.addEventListener('submit', e => {
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
