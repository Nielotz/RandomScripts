(() => {
  // SFI-specific selectors
  const eventCardClass = 'bg-zinc-700';
  const modalSelector = '.fixed.inset-0.z-\\[100\\]';
  const backdropSelector = '.absolute.inset-0.bg-black';
  const rowSelector = '.relative.h-40.border-b.border-zinc-700';

  // State
  const deletedEvents = [];
  const redoStack = [];
  const descriptionCache = new Map();
  const allExtractedEvents = [];

  function getEventCards() {
    return Array.from(document.querySelectorAll(`div.${eventCardClass}.absolute.rounded-xl`))
      .filter(el => document.body.contains(el) && el.dataset.hidden !== '1');
  }

  function addDeleteButtons() {
    const cards = getEventCards();
    cards.forEach((el) => {
      if (el.dataset.deleteBtnAdded) return;
      el.dataset.deleteBtnAdded = '1';

      const btn = document.createElement('button');
      btn.textContent = '✕';
      btn.title = 'Remove this event (Ctrl+Z to undo, Ctrl+Y to redo)';
      btn.style.cssText = `
        position: absolute;
        top: 2px;
        right: 2px;
        z-index: 9999;
        background: rgba(200,50,50,0.85);
        color: white;
        border: none;
        border-radius: 3px;
        padding: 1px 5px;
        font-size: 11px;
        cursor: pointer;
        line-height: 1.2;
      `;
      btn.addEventListener('click', (ev) => {
        ev.stopPropagation();
        ev.preventDefault();
        deletedEvents.push(el);
        redoStack.length = 0;
        const title = getCardTitle(el);
        el.dataset.hidden = '1';
        el.style.display = 'none';
        console.log(`Deleted: ${title} | Undo: ${deletedEvents.length} | Redo: ${redoStack.length}`);
      });

      el.appendChild(btn);
    });
    console.log('Delete buttons added to', cards.length, 'events');
  }

  function getCardTitle(cardEl) {
    try {
      const content = cardEl.querySelector('.pl-6');
      return content?.children[1]?.innerText?.trim().slice(0, 50) || '(unknown)';
    } catch { return '(unknown)'; }
  }

  function undoDelete() {
    if (deletedEvents.length === 0) { console.log('Nothing to undo'); return; }
    const el = deletedEvents.pop();
    el.dataset.hidden = '';
    el.style.display = '';
    redoStack.push(el);
    console.log(`Restored: ${getCardTitle(el)} | Undo: ${deletedEvents.length} | Redo: ${redoStack.length}`);
  }

  function redoDelete() {
    if (redoStack.length === 0) { console.log('Nothing to redo'); return; }
    const el = redoStack.pop();
    deletedEvents.push(el);
    el.dataset.hidden = '1';
    el.style.display = 'none';
    console.log(`Re-deleted: ${getCardTitle(el)} | Undo: ${deletedEvents.length} | Redo: ${redoStack.length}`);
  }

  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'z') { e.preventDefault(); undoDelete(); }
    if (e.ctrlKey && e.key === 'y') { e.preventDefault(); redoDelete(); }
  });

  const delay = ms => new Promise(r => setTimeout(r, ms));

  function getEventDataFromCard(cardEl) {
    const content = cardEl.querySelector('.pl-6');
    if (!content) return null;
    const children = content.children;
    const category = children[0]?.innerText?.trim() || '';
    const title = children[1]?.innerText?.trim() || '';
    const timeText = children[2]?.innerText?.trim() || '';
    const speaker = children[3]?.innerText?.trim() || '';
    const [start, end] = timeText.split(' - ').map(t => t.trim());
    return { category, title, start, end, speaker };
  }

  function buildRoomMap() {
    const rows = Array.from(document.querySelectorAll(rowSelector));
    const map = new Map();
    if (rows.length === 0) return map;

    // Strategy 1: Room label is a non-timeline child inside each row
    for (const row of rows) {
      for (const child of row.children) {
        if (child.classList.contains('pl-32')) continue;
        if (child.classList.contains('absolute') && child.classList.contains('border-l')) continue;
        const text = child.innerText?.trim();
        if (text && text.length < 80 && !text.includes('✕') && !/\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}/.test(text)) {
          map.set(row, text);
          break;
        }
      }
    }
    if (map.size > 0) { console.log('Room map (in-row):', map.size, 'rooms'); return map; }

    // Strategy 2: Room labels are in a parallel sibling column (same parent level)
    const rowsParent = rows[0].parentElement;
    const grandparent = rowsParent?.parentElement;
    if (grandparent) {
      for (const sibling of grandparent.children) {
        if (sibling === rowsParent) continue;
        // Look for a container whose direct children map 1:1 to rows
        const labels = Array.from(sibling.children);
        if (labels.length >= rows.length) {
          let valid = 0;
          for (let i = 0; i < rows.length; i++) {
            const text = labels[i]?.innerText?.trim();
            if (text && text.length < 80 && !text.includes('✕')) valid++;
          }
          if (valid === rows.length) {
            for (let i = 0; i < rows.length; i++) {
              map.set(rows[i], labels[i].innerText.trim());
            }
            console.log('Room map (sibling column):', map.size, 'rooms');
            return map;
          }
        }
      }
    }

    // Strategy 3: Room labels are inside a sibling of each row's parent with matching structure
    if (grandparent) {
      for (const sibling of grandparent.children) {
        if (sibling === rowsParent) continue;
        const labelRows = sibling.querySelectorAll(rowSelector);
        if (labelRows.length === rows.length) {
          for (let i = 0; i < rows.length; i++) {
            const text = labelRows[i]?.innerText?.trim();
            if (text && text.length < 80) map.set(rows[i], text);
          }
          if (map.size > 0) {
            console.log('Room map (parallel rows):', map.size, 'rooms');
            return map;
          }
        }
      }
    }

    console.log('Room map: 0 rooms found (LOCATION will be empty)');
    return map;
  }

  function getRoomName(cardEl, roomMap) {
    const row = cardEl.closest(rowSelector);
    if (!row) return null;
    return roomMap.get(row) || null;
  }

  function getDescriptionFromModal() {
    try {
      const modal = document.querySelector(modalSelector);
      if (!modal) return null;
      const descDiv = modal.querySelector('.mt-4');
      if (!descDiv) return null;
      const descP = descDiv.querySelector('p');
      return descP?.innerText?.trim() || null;
    } catch { return null; }
  }

  async function extractEvents(eventDate = null) {
    if (!eventDate) {
      console.log('Usage: calendarHelper.extractEvents("YYYY-MM-DD")');
      return;
    }
    let parsedDate;
    try {
      parsedDate = new Date(eventDate);
      if (isNaN(parsedDate.getTime())) throw new Error();
    } catch {
      console.log('Invalid date. Use format: YYYY-MM-DD');
      return;
    }
    const eventDateStr = parsedDate.toISOString().split('T')[0];
    const todayStr = new Date().toISOString().split('T')[0];
    if (eventDateStr < todayStr) {
      console.log('Date is in the past. Exiting.');
      return;
    }

    console.log('Extracting events for:', eventDateStr);
    const cards = getEventCards();
    console.log('Found', cards.length, 'events to extract');
    const roomMap = buildRoomMap();

    const results = [];
    let cachedCount = 0;
    let scrapedCount = 0;

    for (let i = 0; i < cards.length; i++) {
      const card = cards[i];
      if (!document.body.contains(card)) { console.log(i, 'skipped (removed)'); continue; }

      const data = getEventDataFromCard(card);
      if (!data) { console.log(i, 'skipped (no data)'); continue; }

      const room = getRoomName(card, roomMap);
      const cacheKey = `${data.title}|${data.start}|${data.end}`;

      if (descriptionCache.has(cacheKey)) {
        results.push({ ...data, room, date: eventDateStr, description: descriptionCache.get(cacheKey) });
        cachedCount++;
        console.log(i, 'cached:', data.title?.slice(0, 40));
        continue;
      }

      console.log(i, 'clicking:', data.title?.slice(0, 50));
      card.click();

      // Wait for modal
      let modal = null;
      for (let tries = 0; tries < 30; tries++) {
        await delay(100);
        modal = document.querySelector(modalSelector);
        if (modal) break;
      }
      if (!modal) {
        console.warn(i, 'no modal appeared');
        results.push({ ...data, room, date: eventDateStr, description: null, _failed: true });
        continue;
      }

      await delay(150);
      const description = getDescriptionFromModal();
      descriptionCache.set(cacheKey, description);

      results.push({ ...data, room, date: eventDateStr, description });
      scrapedCount++;
      console.log(i, 'scraped:', data.title?.slice(0, 40));

      // Close modal by clicking backdrop
      const backdrop = modal.querySelector(backdropSelector);
      if (backdrop) {
        backdrop.click();
      } else {
        // Fallback: click close button
        const closeBtn = modal.querySelector('button');
        if (closeBtn) closeBtn.click();
      }

      // Wait for modal to close
      for (let tries = 0; tries < 20; tries++) {
        await delay(50);
        if (!document.querySelector(modalSelector)) break;
      }
      await delay(100);
    }

    allExtractedEvents.push(...results);

    const json = JSON.stringify(results, null, 2);
    try {
      await navigator.clipboard.writeText(json);
      console.log('✓ Copied', results.length, 'events to clipboard');
    } catch {
      console.log('Clipboard failed, data is in window.extractedEvents');
    }

    window.extractedEvents = results;
    console.log(`Done! ${cachedCount} cached, ${scrapedCount} scraped. Total accumulated: ${allExtractedEvents.length}`);
    return results;
  }

  // ICS generation
  function escapeICS(str) {
    if (!str) return '';
    return str
      .replace(/\\/g, '\\\\')
      .replace(/;/g, '\\;')
      .replace(/,/g, '\\,')
      .replace(/\n/g, '\\n');
  }

  function generateUID() {
    return 'sfi-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9) + '@calendar';
  }

  function formatICSDate(dateStr, timeStr) {
    const [hours, minutes] = timeStr.split(':');
    const date = dateStr.replace(/-/g, '');
    return `${date}T${hours.padStart(2, '0')}${minutes.padStart(2, '0')}00`;
  }

  function generateICS(events) {
    const lines = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//SFI Calendar Helper//EN',
      'CALSCALE:GREGORIAN',
      'METHOD:PUBLISH',
      'X-WR-CALNAME:Studencki Festiwal Informatyczny'
    ];

    for (const event of events) {
      if (event._failed) continue;
      if (!event.start || !event.end || !event.date) continue;

      const dtStart = formatICSDate(event.date, event.start);
      const dtEnd = formatICSDate(event.date, event.end);
      const uid = generateUID();
      const now = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';

      const descParts = [];
      if (event.speaker) descParts.push(`Speaker: ${event.speaker}`);
      if (event.category) descParts.push(`Category: ${event.category}`);
      if (event.description) descParts.push('', event.description);
      const fullDescription = descParts.join('\n');

      lines.push('BEGIN:VEVENT');
      lines.push(`UID:${uid}`);
      lines.push(`DTSTAMP:${now}`);
      lines.push(`DTSTART:${dtStart}`);
      lines.push(`DTEND:${dtEnd}`);
      lines.push(`SUMMARY:${escapeICS(event.title)}`);
      if (event.room) lines.push(`LOCATION:${escapeICS(event.room)}`);
      if (fullDescription) lines.push(`DESCRIPTION:${escapeICS(fullDescription)}`);
      lines.push('END:VEVENT');
    }

    lines.push('END:VCALENDAR');
    return lines.join('\r\n');
  }

  function downloadICS(events = null, filename = null) {
    events = events || allExtractedEvents;
    if (!events || events.length === 0) {
      console.error('No events to export! Run extractEvents() first.');
      return;
    }

    if (!filename) filename = 'sfi-events.ics';

    const icsContent = generateICS(events);
    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    console.log('✓ Downloaded', filename, 'with', events.filter(e => !e._failed).length, 'events');
  }

  function clearEvents() {
    allExtractedEvents.length = 0;
    console.log('Cleared all accumulated events.');
  }

  window.calendarHelper = { addDeleteButtons, extractEvents, undoDelete, redoDelete, downloadICS, clearEvents, generateICS };
  addDeleteButtons();
  console.log('SFI Calendar Helper ready!');
  console.log('  1. Delete unwanted events (Ctrl+Z undo, Ctrl+Y redo)');
  console.log('  2. calendarHelper.extractEvents("YYYY-MM-DD") — scrape visible events');
  console.log('  3. Switch day tab → calendarHelper.addDeleteButtons() → repeat');
  console.log('  4. calendarHelper.downloadICS() — download combined .ics for all extracted days');
})();
