// Members area dashboard (mockup). Sample member data; in production this would come from
// the email platform (EMX / ActiveCampaign) contact record plus site analytics.
(function () {
  const U = 'https://www.mobileeurope.co.uk/wp-content/uploads/';
  const $ = id => document.getElementById(id);
  const esc = t => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };

  const m = window.ME_MEMBER && ME_MEMBER.get();
  if (!m) { $('mem-locked').hidden = false; return; }
  $('mem-dash').hidden = false;

  // ---------- Greeting: "Hello" on the first visit, "Welcome back" after that ----------
  const visits = store.get('me-visits', 0);
  $('mem-greet').textContent = (visits ? 'Welcome back, ' : 'Hello, ') + m.first;
  store.set('me-visits', visits + 1);
  $('mem-av').textContent = m.first[0] + m.last[0];
  $('mem-meta').textContent = `${m.title} · ${m.company} · Member since ${m.since}`;
  $('mem-logout').addEventListener('click', () => { ME_MEMBER.logout(); location.href = 'index.html'; });

  // ---------- Sample activity ----------
  const downloads = [
    { t: 'OSS: Why trusted data matters as a catalyst for AI modernisation', kind: 'Independent Research', date: '13 Nov 2026', img: '2026/10/ME-Report-BLUEPLANET-COVER-v1.jpg', href: 'research.html' },
    { t: 'Detecting and Countering Fraud and Revenue Leakage in Mobile Networks', kind: 'Handbook · ENEA', date: '11 Nov 2026', img: '2026/11/Detecting-and-Countering-Fraud-and-Revenue-Leakage-in-Mobile-Networks-Handbook-for-Fraud-Revenue-Assurance-Network-Teams-1-1-696x905.jpg', href: 'white-papers.html' },
    { t: 'Agentic AI: Achieving autonomous network operations', kind: 'Independent Research', date: '14 Oct 2026', img: '2026/03/ME-Report-Celfocus26-COVER.jpg', href: 'research.html' },
    { t: 'There’s a Core for That', kind: 'White paper · Mavenir', date: '2 Oct 2026', img: '2026/09/ISS-OnOff-Telecom-Case-Study-3-WP-696x844.jpg', href: 'white-papers.html' },
    { t: '5G Advanced: Will 5G’s second wave deliver value?', kind: 'Independent Research', date: '18 Aug 2026', img: '2025/02/ME-Report-5GAdvanced-COVER-tint-v1.jpg', href: 'research.html' }
  ];
  const upcoming = [
    { t: 'AI in Network Optimisation: Finding Forgotten Revenue', when: 'Tue 24 Nov 2026 · 09:30 GMT', date: '2026-11-24', series: 'The Briefing · AI', href: 'briefing-event.html' },
    { t: 'Telecoms in Focus', when: 'Thu 10 Dec 2026 · Virtual conference', date: '2026-12-10', series: 'Mobile Europe event', href: 'events.html' }
  ];
  const attended = [
    { t: 'Can a cloud- and AI-native operator exist?', date: '12 Nov 2026', img: '2026/10/ME-BRIEFING-cloud2-ADS-v1--600x350.jpg' },
    { t: 'Does 5G Standalone stand up – is the support role of digital twins key?', date: '27 Oct 2026', img: '2026/07/ME-BRIEFING-5G-4-ADS-v1-600x350.jpg' },
    { t: 'Digital sovereignty in telecoms', date: '1 Oct 2026', img: '2026/07/ME-BRIEFING-SECURITY-2-ADS-v1-600x350.jpg' }
  ];
  const reading = [
    { t: 'Data centres must look beyond the ‘bragawatts’ race, says Pulsant CEO', img: '2026/11/Rob-Coupland-ME.png', pct: 64 },
    { t: 'Cellnex UK MD on ‘catching up’ with Europe’s 5G networks', img: '2026/11/Steve-Cray.png', pct: 35 },
    { t: 'Mavenir CRO on why AI is putting the mobile core back in focus', img: '2026/10/Dejan-Leskaoski.png', pct: 80 }
  ];
  const ARTICLES_READ = 14;

  // ---------- Topics (tag cloud). Extra interests map onto site categories for recommendations ----------
  const TOPICS = [
    ['5G & Beyond', 5], ['Access', 3], ['Automation/AI', 5], ['BSS/OSS/CX', 3], ['Cloud/NFV', 4], ['Digital Platforms & APIs', 3],
    ['Edge', 4], ['Financial/Regulation', 3], ['Optical/IP', 3], ['RAN', 5], ['Satellite', 3], ['Security', 4], ['Sustainability', 2],
    ['Open RAN', 4, 'RAN'], ['AI-RAN', 4, 'RAN'], ['Private 5G', 3, 'Edge'], ['6G', 4, '5G & Beyond'], ['Data centres', 4, 'Cloud/NFV'],
    ['Digital sovereignty', 3, 'Security'], ['Fraud & revenue assurance', 2, 'BSS/OSS/CX'], ['Direct-to-device', 2, 'Satellite'],
    ['Network APIs', 3, 'Digital Platforms & APIs'], ['Autonomous networks', 4, 'Automation/AI'], ['Fibre', 3, 'Access'],
    ['Subsea cables', 2, 'Optical/IP'], ['M&A and deals', 3, 'Financial/Regulation'], ['Energy efficiency', 2, 'Sustainability']
  ];
  const catOf = name => { const t = TOPICS.find(x => x[0] === name); return t ? (t[2] || t[0]) : name; };
  let followed = store.get('me-topics', ['Automation/AI', 'RAN', 'Edge', 'Security', 'Open RAN', 'Data centres']);

  // ---------- Stats ----------
  function renderStats() {
    const stats = [[downloads.length, 'Downloads'], [attended.length, 'Briefings attended'], [ARTICLES_READ, 'Articles read this month'], [followed.length, 'Topics followed']];
    $('mem-stats').innerHTML = stats.map(([n, l]) => `<div class="stat"><b>${n}</b><span>${l}</span></div>`).join('');
  }

  // ---------- Recommendations from followed topics (round-robin across categories, newest first) ----------
  function renderRecs() {
    const cats = [...new Set(followed.map(catOf))];
    const pools = cats.map(c => (window.ME_STORIES[c] || []).map(s => ({ ...s, cat: c })));
    const seen = new Set(reading.map(r => r.t)), picks = [];
    for (let i = 0; picks.length < 6 && i < 12; i++) {
      pools.forEach(p => { const s = p[i]; if (s && !seen.has(s.t) && picks.length < 6) { seen.add(s.t); picks.push(s); } });
    }
    $('rec-why').textContent = cats.length ? `Based on ${cats.length} topic${cats.length > 1 ? 's' : ''} you follow` : 'Follow some topics to get recommendations';
    $('rec-grid').innerHTML = picks.length ? picks.map(s => `
      <a class="rec" href="article.html">
        <span class="rec-pic"><img src="${U}${s.img}" alt="" loading="lazy"></span>
        <span class="rec-why">Because you follow ${esc(s.cat)}</span>
        <b>${esc(s.t)}</b>
        <small>${esc(s.date)}</small>
      </a>`).join('') : '<p class="mem-empty">Pick a few topics on the right and we’ll suggest articles here.</p>';
  }

  // ---------- Tag cloud ----------
  function renderCloud() {
    $('tag-cloud').innerHTML = TOPICS.map(([name, w]) => {
      const on = followed.includes(name);
      return `<button type="button" class="tcl w${w}${on ? ' on' : ''}" aria-pressed="${on}" data-topic="${esc(name)}">${on ? '✓ ' : '+ '}${esc(name)}</button>`;
    }).join('');
    $('topic-count').textContent = `${followed.length} followed`;
  }
  $('tag-cloud').addEventListener('click', e => {
    const b = e.target.closest('.tcl'); if (!b) return;
    const name = b.dataset.topic;
    followed = followed.includes(name) ? followed.filter(x => x !== name) : [...followed, name];
    store.set('me-topics', followed);
    renderCloud(); renderRecs(); renderStats(); renderSuggested();
    const again = $('tag-cloud').querySelector(`[data-topic="${CSS.escape(name)}"]`); if (again) again.focus();
  });

  // ---------- Events ----------
  function daysTo(iso) { const [y, mo, d] = iso.split('-').map(Number); const t = new Date(); t.setHours(0, 0, 0, 0); return Math.round((new Date(y, mo - 1, d) - t) / 864e5); }
  $('mem-events').innerHTML = `
    <h3 class="mem-h3">Registered</h3>
    ${upcoming.map(ev => { const n = daysTo(ev.date); return `
      <div class="ev-row">
        <span class="ev-badge">${n === 0 ? 'Today' : n === 1 ? 'Tomorrow' : 'In ' + n + ' days'}</span>
        <div class="ev-info"><small>${esc(ev.series)}</small><a href="${ev.href}"><b>${esc(ev.t)}</b></a><span>${esc(ev.when)}</span></div>
        <div class="ev-btns"><a class="btn pink" href="${ev.href}">Joining details</a><a class="btn ghost" href="#">Add to calendar</a></div>
      </div>`; }).join('')}
    <h3 class="mem-h3">Attended</h3>
    <div class="att-grid">${attended.map(a => `
      <a class="att" href="events.html"><span class="att-pic"><img src="${U}${a.img}" alt="" loading="lazy"><span class="play" aria-hidden="true"></span></span><b>${esc(a.t)}</b><small>Attended ${esc(a.date)} · Watch on demand</small></a>`).join('')}</div>`;

  // ---------- Downloads ----------
  $('mem-downloads').innerHTML = `<ul class="dl-list">${downloads.map(d => `
    <li><img src="${U}${d.img}" alt="" loading="lazy"><div><b>${esc(d.t)}</b><small>${esc(d.kind)} · Downloaded ${esc(d.date)}</small></div><a class="btn ghost" href="${d.href}">Download again</a></li>`).join('')}</ul>`;

  // ---------- Continue reading ----------
  $('mem-reading').innerHTML = reading.map(r => `
    <a class="read" href="article.html"><img src="${U}${r.img}" alt="" loading="lazy"><div><b>${esc(r.t)}</b><span class="bar"><i style="width:${r.pct}%"></i></span><small>${r.pct}% read</small></div></a>`).join('');

  // ---------- Suggested Briefings (matched to followed topics) ----------
  const BRIEFINGS = [
    { t: 'The critical role of telcos in defence', date: '2027-02-04', label: '4 Feb 2027', topics: ['Security', 'Digital sovereignty'], spons: 'Red Hat' },
    { t: 'Extracting the full potential of 5G Standalone', date: '2027-04-15', label: '15 Apr 2027', topics: ['5G & Beyond', 'RAN', '6G', 'Open RAN', 'AI-RAN', 'Private 5G'] },
    { t: 'Telco Automation & AI', date: '2027-04-22', label: '22 Apr 2027', topics: ['Automation/AI', 'Autonomous networks', 'AI-RAN'], spons: 'Red Hat' },
    { t: 'Delivering a Cloud-native Telco', date: '2027-05-27', label: '27 May 2027', topics: ['Cloud/NFV', 'Data centres', 'Edge'] }
  ];
  let registered = store.get('me-registered', []);
  function renderSuggested() {
    const list = BRIEFINGS.filter(b => b.topics.some(t => followed.includes(t)));
    $('mem-suggest-events').innerHTML = list.length ? list.map(b => {
      const done = registered.includes(b.t);
      const match = b.topics.find(t => followed.includes(t));
      return `<div class="sug"><small>${esc(b.label)} · matches ${esc(match)}</small><b>${esc(b.t)}</b>
        <button type="button" class="btn ${done ? 'ghost' : 'pink'} sug-reg" data-b="${esc(b.t)}" ${done ? 'aria-pressed="true"' : ''}>${done ? '✓ Registered' : 'Register in one click'}</button></div>`;
    }).join('') : '<p class="mem-empty">Follow topics to see matching Briefings.</p>';
  }
  $('mem-suggest-events').addEventListener('click', e => {
    const b = e.target.closest('.sug-reg'); if (!b) return;
    const t = b.dataset.b;
    registered = registered.includes(t) ? registered.filter(x => x !== t) : [...registered, t];
    store.set('me-registered', registered); renderSuggested();
  });

  // ---------- Email preferences ----------
  const PREFS = [['daily', 'Daily news', 'Weekday mornings'], ['insights', 'Weekly Insights', 'Interviews and analysis, Fridays'],
    ['briefing', 'The Briefing alerts', 'New events and reminders'], ['research', 'Independent Research', 'New reports'], ['partners', 'Partner offers', 'Occasional, from our sponsors']];
  let prefs = store.get('me-prefs', { daily: true, insights: true, briefing: true, research: true, partners: false });
  $('mem-prefs').innerHTML = PREFS.map(([k, l, d]) => `
    <label class="pref"><span><b>${l}</b><small>${d}</small></span><input type="checkbox" role="switch" data-k="${k}" ${prefs[k] ? 'checked' : ''}><i aria-hidden="true"></i></label>`).join('') +
    '<p class="mem-help" id="pref-saved">Changes save automatically and would sync to EMX / ActiveCampaign.</p>';
  $('mem-prefs').addEventListener('change', e => {
    const k = e.target.dataset.k; if (!k) return;
    prefs[k] = e.target.checked; store.set('me-prefs', prefs);
    const s = $('pref-saved'); s.textContent = '✓ Saved'; setTimeout(() => { s.textContent = 'Changes save automatically and would sync to EMX / ActiveCampaign.'; }, 1600);
  });

  renderStats(); renderCloud(); renderRecs(); renderSuggested();
})();
