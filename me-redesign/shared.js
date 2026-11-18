// Shared header, footer and mockup toolbar for all pages
(function () {
  const page = document.body.dataset.page;      // home | cat | brief | res
  const cat = document.body.dataset.cat || '';
  const IMG = 'https://www.mobileeurope.co.uk/wp-content/uploads/';
  window.ME_IMG = IMG;

  const cats = ['5G & Beyond', 'Access', 'Automation/AI', 'BSS/OSS/CX', 'Cloud/NFV', 'Digital Platforms & APIs', 'Edge', 'Financial/Regulation', 'Optical/IP', 'RAN', 'Satellite', 'Security', 'Sustainability'];

  const header = `
  <div class="util"><div class="wrap">
    <div class="nb">
      <b>Next Briefing</b>
      <span>Tue 24 Nov · <em>AI in Network Optimisation: Finding Forgotten Revenue</em> · Live online, 09:30 GMT</span>
      <a href="the-briefing.html">Register free</a>
    </div>
    <div class="right"><a href="#">Newsletter</a><a href="#">Advertise</a><a href="#">About</a></div>
  </div></div>
  <div class="lb-zone"><div class="ad-label">Advertisement</div><div class="ad ad-lb">Leaderboard (LB)<small>728×90 · GAM · 320×50 on mobile</small></div></div>
  <div class="mast"><div class="wrap">
    <a class="logo" href="index.html" aria-label="Mobile Europe home">
      <span class="mark">ME</span>
      <span class="word"><b>Mobile Europe</b><small>Communications infrastructure and digital services in EMEA</small></span>
    </a>
    <div class="franchises">
      <a class="fr brief" href="the-briefing.html"><small>Live events</small><b>The Briefing</b><span>Next: 24 Nov · AI &amp; Revenue</span></a>
      <a class="fr res" href="research.html"><small>Reports</small><b>Independent<br>Research</b><span>New: OSS &amp; AI modernisation</span></a>
    </div>
    <div class="mast-tools"><input class="search" placeholder="Search" aria-label="Search"><a class="btn red" href="#">Subscribe</a></div>
    <button class="burger" aria-label="Menu">☰</button>
  </div></div>
  <div class="nav"><div class="wrap">
    <a href="index.html" class="${page === 'home' ? 'on' : ''}">Home</a>
    <a href="#">News</a><a href="#">Insights</a><a href="#">CxO Zone</a><a href="#">White Paper Hub</a><a href="#">Videos</a><a href="#">Events</a>
    <span class="sep"></span>
    <a href="the-briefing.html" class="f-brief ${page === 'brief' ? 'on' : ''}">The Briefing</a>
    <a href="research.html" class="f-res ${page === 'res' ? 'on' : ''}">Research</a>
  </div></div>
  <div class="cats"><div class="wrap">
    ${cats.map(c => `<a href="${c === '5G & Beyond' ? 'category-5g.html' : '#'}" class="${c === cat ? 'on' : ''}">${c.replace('&', '&amp;')}</a>`).join('')}
  </div></div>`;

  const footer = `
  <footer class="site"><div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="index.html" style="color:#fff"><span class="mark">ME</span><span class="word"><b>Mobile Europe</b></span></a>
        <p style="margin-top:12px;max-width:300px">Covering communications infrastructure and digital services in EMEA.</p>
      </div>
      <div><h5>Editorial</h5><a href="#">News</a><a href="#">Insights</a><a href="#">CxO Zone</a><a href="#">White Paper Hub</a><a href="#">Videos</a></div>
      <div><h5>Franchises</h5><a href="the-briefing.html">The Briefing</a><a href="research.html">Independent Research</a><a href="#">Telecoms in Focus</a><a href="#">Events</a></div>
      <div><h5>Company</h5><a href="#">About</a><a href="#">Advertise</a><a href="#">Editorial Advisory Board</a><a href="#">Contact</a><a href="#">Privacy</a></div>
    </div>
    <div class="legal">Design mockup: not the live site. Content and images from mobileeurope.co.uk, used for layout only.</div>
  </div></footer>`;

  const pages = [['index.html', 'home', 'Homepage'], ['category-5g.html', 'cat', '5G & Beyond'], ['the-briefing.html', 'brief', 'The Briefing'], ['research.html', 'res', 'Research']];
  const toolbar = `<div class="mock">
    <span class="lbl" style="padding:0 6px;color:#888">Mockup</span>
    ${pages.map(p => `<a href="${p[0]}" class="${p[1] === page ? 'on' : ''}">${p[2]}</a>`).join('')}
  </div>`;

  document.getElementById('site-header').outerHTML = header;
  document.getElementById('site-footer').outerHTML = footer + toolbar;

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

// Small pin icon used by pages
window.PIN = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16 3l5 5-3 1-4 4 1 5-2 2-4-4-5 5-1-1 5-5-4-4 2-2 5 1 4-4z"/></svg>';
document.querySelectorAll('[data-pin]').forEach(el => el.insertAdjacentHTML('afterbegin', window.PIN));
