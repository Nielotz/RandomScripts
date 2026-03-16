// WDI Agenda to .ics exporter — paste into browser console
(function () {
  'use strict';

  const EVENT_DATE = '2026-03-20'; // YYYY-MM-DD

  // ── Avoid double-injection ──
  if (document.getElementById('ics-export-btn')) {
    alert('Script already injected.');
    return;
  }

  // ── Inject styles to force checkbox visibility ──
  const style = document.createElement('style');
  style.textContent = `
    .ics-select-cb {
      position: absolute !important;
      left: 6px !important;
      top: 10px !important;
      width: 20px !important;
      height: 20px !important;
      cursor: pointer !important;
      accent-color: #e74c3c !important;
      z-index: 10 !important;
      margin: 0 !important;
      opacity: 1 !important;
      visibility: visible !important;
      display: block !important;
      appearance: auto !important;
      -webkit-appearance: checkbox !important;
      pointer-events: auto !important;
      clip: auto !important;
      clip-path: none !important;
      overflow: visible !important;
      transform: none !important;
    }
  `;
  document.head.appendChild(style);

  // ── Inject checkboxes into every event ──
  const headers = document.querySelectorAll('.agenda_header');
  headers.forEach((header) => {
    header.style.position = 'relative';
    header.style.paddingLeft = '36px';

    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.className = 'ics-select-cb';
    header.insertBefore(cb, header.firstChild);
  });

  // ── Floating toolbar ──
  const bar = document.createElement('div');
  bar.id = 'ics-export-btn';
  bar.style.cssText =
    'position:fixed;bottom:20px;right:20px;z-index:99999;display:flex;gap:8px;' +
    'background:#222;padding:10px 14px;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,.4);' +
    'font-family:system-ui,sans-serif;align-items:center;';

  const selAllBtn = mkBtn('Select all', '#3498db');
  const selNoneBtn = mkBtn('Select none', '#95a5a6');
  const countLabel = document.createElement('span');
  countLabel.style.cssText = 'color:#fff;font-size:13px;min-width:30px;text-align:center;';
  const exportBtn = mkBtn('Export .ics', '#27ae60');

  bar.append(selAllBtn, selNoneBtn, countLabel, exportBtn);
  document.body.appendChild(bar);

  function mkBtn(text, bg) {
    const b = document.createElement('button');
    b.textContent = text;
    b.style.cssText =
      `background:${bg};color:#fff;border:none;padding:8px 14px;border-radius:6px;` +
      'cursor:pointer;font-size:13px;font-weight:600;';
    return b;
  }

  // ── Select helpers ──
  function allCbs() { return document.querySelectorAll('.ics-select-cb'); }
  function updateCount() {
    const n = document.querySelectorAll('.ics-select-cb:checked').length;
    countLabel.textContent = n + ' sel.';
  }
  document.addEventListener('change', (e) => {
    if (e.target.classList.contains('ics-select-cb')) updateCount();
  });
  selAllBtn.addEventListener('click', () => { allCbs().forEach(c => { c.checked = true; }); updateCount(); });
  selNoneBtn.addEventListener('click', () => { allCbs().forEach(c => { c.checked = false; }); updateCount(); });
  updateCount();

  // ── Export logic ──
  exportBtn.addEventListener('click', async () => {
    const selected = [];
    allCbs().forEach((cb) => {
      if (cb.checked) selected.push(cb.closest('.agenda_header'));
    });
    if (!selected.length) { alert('No events selected.'); return; }

    exportBtn.disabled = true;
    const events = [];

    for (let i = 0; i < selected.length; i++) {
      exportBtn.textContent = `Loading ${i + 1}/${selected.length}…`;
      events.push(await extractEvent(selected[i]));
    }

    const ics = buildICS(events);
    download('wdi-agenda.ics', ics);

    exportBtn.textContent = 'Export .ics';
    exportBtn.disabled = false;
  });

  // ── Find the details panel for a given header ──
  function findDetailsPanel(header) {
    const inp = header.querySelector('input[id^="checkReg"], input[id^="checkFav"]');
    if (inp) {
      const uuid = inp.id.replace(/^check(Reg|Fav)/, '');
      return document.getElementById('subject_' + uuid);
    }
    return header.nextElementSibling;
  }

  // ── Extract event data from .agenda_header ──
  async function extractEvent(header) {
    const aside = header.querySelector('.header_aside');

    const times = aside.querySelectorAll('span.time time.ng-binding');
    const startTime = times[0] ? times[0].textContent.trim() : '00:00';
    const endTime = times[1] ? times[1].textContent.trim() : '00:00';

    const locEl = aside.querySelector('span.location');
    const location = locEl
      ? locEl.textContent.replaceAll(/\s+/g, ' ').trim()
      : '';

    const titleLink = header.querySelector('a.js-header_title');
    const h6 = titleLink.querySelector('h6');
    const badge = h6.querySelector('.agenda_badge');
    const title = h6.textContent
      .replace(badge ? badge.textContent : '', '')
      .replaceAll(/\s+/g, ' ')
      .trim();

    const trackEl = titleLink.querySelector('small.agenda_header__track');
    const track = trackEl ? trackEl.textContent.replaceAll(/\s+/g, ' ').trim() : '';

    const speakerEls = titleLink.querySelectorAll('ul.js-header_speakers li');
    const speakers = [...new Set([...speakerEls].map((li) => {
      const name = li.querySelector('.name');
      return name ? name.childNodes[0].textContent.trim() : '';
    }).filter(Boolean))];

    const description = await extractDescription(header, titleLink);

    return { startTime, endTime, location, title, track, speakers, description };
  }

  async function extractDescription(header, titleLink) {
    const panel = findDetailsPanel(header);
    if (!panel) return '';

    const descEl = panel.querySelector('.details_description small');
    if (!descEl) return '';

    // Use description if already populated (event was previously expanded)
    const existing = descEl.textContent.trim();
    if (existing) return existing.replaceAll(/\s+/g, ' ');

    // Click to expand — Angular will load the description via ng-bind-html
    titleLink.click();

    // Poll until descEl gets content (up to 5s)
    const text = await poll(() => {
      const t = descEl.textContent.trim();
      return t || null;
    }, 5000);

    return text ? text.replaceAll(/\s+/g, ' ') : '';
  }

  function poll(fn, timeoutMs) {
    return new Promise((resolve) => {
      const start = Date.now();
      const check = () => {
        const result = fn();
        if (result != null) { resolve(result); return; }
        if (Date.now() - start > timeoutMs) { resolve(null); return; }
        setTimeout(check, 200);
      };
      setTimeout(check, 300);
    });
  }

  // ── Build .ics content ──
  function buildICS(events) {
    const lines = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//WDI Agenda Exporter//EN',
      'CALSCALE:GREGORIAN',
      'METHOD:PUBLISH',
    ];

    for (const ev of events) {
      const dtStart = toICSDateTime(EVENT_DATE, ev.startTime);
      const dtEnd = toICSDateTime(EVENT_DATE, ev.endTime);
      const uid = crypto.randomUUID() + '@wdi-export';

      const descParts = [];
      if (ev.track) descParts.push(ev.track);
      if (ev.speakers.length) descParts.push('Speakers: ' + ev.speakers.join(', '));
      if (ev.description) descParts.push(ev.description);
      const desc = descParts.join('\n');

      lines.push(
        'BEGIN:VEVENT',
        'DTSTART;TZID=Europe/Warsaw:' + dtStart,
        'DTEND;TZID=Europe/Warsaw:' + dtEnd,
        'SUMMARY:' + icsEscape(ev.title),
        'LOCATION:' + icsEscape(ev.location),
        ...(desc ? ['DESCRIPTION:' + icsEscape(desc)] : []),
        'UID:' + uid,
        'END:VEVENT',
      );
    }

    lines.push('END:VCALENDAR');
    return lines.join('\r\n');
  }

  function toICSDateTime(date, time) {
    return date.replaceAll('-', '') + 'T' + time.replace(':', '') + '00';
  }

  function icsEscape(str) { // NOSONAR
    return str
      .replaceAll('\\', '\\\\')
      .replaceAll(';', '\\;')
      .replaceAll(',', '\\,')
      .replaceAll('\n', '\\n');
  }

  function download(filename, text) {
    const blob = new Blob([text], { type: 'text/calendar;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { a.remove(); URL.revokeObjectURL(a.href); }, 100);
  }

  console.log('[WDI ICS Exporter] Injected. Checkboxes added to ' + headers.length + ' events.');
})();
