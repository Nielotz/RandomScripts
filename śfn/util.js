(() => {
  const eventSelector = '.schedule-event';
  const overlaySelector = '.message-overlay';

  // Undo stack for deleted events
  const deletedEvents = [];

  function addDeleteButtons() {
    const nodes = document.querySelectorAll(eventSelector);
    nodes.forEach((el) => {
      if (el.dataset.deleteBtnAdded) return;
      el.dataset.deleteBtnAdded = '1';

      const btn = document.createElement('button');
      btn.textContent = '✕';
      btn.title = 'Remove this event (Ctrl+Z to undo)';
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
        // Save for undo: element and its position in parent
        const parent = el.parentElement;
        const nextSibling = el.nextElementSibling;
        deletedEvents.push({ element: el, parent, nextSibling });
        el.remove();
        console.log('Event deleted. Press Ctrl+Z to undo. Stack:', deletedEvents.length);
      });

      const pos = getComputedStyle(el).position;
      if (pos === 'static') el.style.position = 'relative';
      el.appendChild(btn);
    });
    console.log('Delete buttons added to', nodes.length, 'events');
  }

  function undoDelete() {
    if (deletedEvents.length === 0) {
      console.log('Nothing to undo');
      return;
    }
    const { element, parent, nextSibling } = deletedEvents.pop();
    if (parent) {
      parent.insertBefore(element, nextSibling);
      console.log('Event restored. Stack:', deletedEvents.length);
    }
  }

  // Listen for Ctrl+Z
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'z') {
      e.preventDefault();
      undoDelete();
    }
  });

  const delay = ms => new Promise(r => setTimeout(r, ms));

  function getDescription() {
    try {
      const upcoming = document.getElementsByClassName("upcoming-events")[0];
      return Array.from(upcoming.children[0].children[1].children).at(-1).children[1].innerText.trim();
    } catch (e) {
      return null;
    }
  }

  function getTimeAndTitle(innerHTML) {
    // innerHTML example: '<b _ngcontent-serverapp-c127="">15:10 - 16:30</b> Poezjoterapia. O leczącej mocy słowa '
    const _timeDesc = innerHTML.split('</b>').map(s => s.trim());
    const time = _timeDesc[0].split('>')[1].trim();
    const startEnd = time.split(' - ').map(t => t.trim());
    const title = _timeDesc[1].trim();
    return { start: startEnd[0], end: startEnd[1], title: title };
  }

  function buildPlaceMap() {
    const places = document.querySelectorAll('.swimline-header')[0].children;
    const map = {};
    for (const place of places) {
      const left = place.style.left || getComputedStyle(place).left;
      map[left] = place.innerText.trim();
    }
    return map;
  }

  function getPlace(eventNode, placeMap) {
    const eventLeft = eventNode.style.left || getComputedStyle(eventNode).left;
    return placeMap[eventLeft] || null;
  }

  async function extractEvents() {
    const nodes = Array.from(document.querySelectorAll(eventSelector)).filter(n => document.body.contains(n));
    console.log('Found', nodes.length, 'events to extract');
    const placeMap = buildPlaceMap();
    const results = [];

    for (let i = 0; i < nodes.length; i++) {
      const n = nodes[i];
      if (!document.body.contains(n)) {
        console.log(i, 'skipped (removed)');
        continue;
      }
      const innerHTML = n.children[0].innerHTML;
      const { start, end, title } = getTimeAndTitle(innerHTML);
      const place = getPlace(n, placeMap);

      console.log(i, 'clicking:', n.innerText.trim().slice(0, 50));

      // Click to open overlay
      n.children[0].click();

      // Wait for overlay to appear
      let overlay = null;
      for (let tries = 0; tries < 30; tries++) {
        await delay(100);
        overlay = document.querySelector(overlaySelector);
        if (overlay) break;
      }
      if (!overlay) {
        console.warn(i, 'no overlay appeared, using node text');
        results.push({ rawText: n.innerText.trim(), _failed: true });
        continue;
      }
      const description = getDescription();

      const scraped = {
        title: title,
        place: place,
        start: start,
        end: end,
        description: description
      };
      results.push(scraped);
      console.log(i, 'scraped:', scraped.title?.slice(0, 40));

      // Close overlay
      overlay.click();

      // Wait for overlay to disappear
      for (let tries = 0; tries < 20; tries++) {
        await delay(50);
        if (!document.querySelector(overlaySelector)) break;
      }

      // Extra delay between events
      await delay(100);
    }

    // Copy to clipboard
    const json = JSON.stringify(results, null, 2);
    try {
      await navigator.clipboard.writeText(json);
      console.log('✓ Copied', results.length, 'events to clipboard!');
    } catch (e) {
      console.log('Clipboard failed, but data is in window.extractedEvents');
    }

    window.extractedEvents = results;
    console.log('Done! Access via window.extractedEvents or paste from clipboard');
    return results;
  }

  window.calendarHelper = { addDeleteButtons, extractEvents, undoDelete };
  addDeleteButtons();
  console.log('Ready! Run: calendarHelper.extractEvents() | Ctrl+Z to undo delete');
})();