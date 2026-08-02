/**
 * @file
 * Rich product cards for Terra Collecta's Scolta search.
 *
 * Registers two Scolta renderers: a result renderer that paints a product's
 * photograph, price and category alongside the title and highlighted excerpt,
 * and a suggestion renderer that puts the same photograph and price on the
 * search-as-you-type rows. Everything they need comes from the search index —
 * the image and price are written by tc_scolta_card_metadata() in
 * functions.php, and the stock status and category by the Scolta plugin's own
 * WooCommerce mapping — so neither a card nor a suggestion costs a per-result
 * server call.
 *
 * Load order matters. scolta.js defines window.Scolta when it executes and
 * calls Scolta.init() on DOMContentLoaded, so this file must run after the
 * former and before the latter. The theme enqueues it at wp_footer with
 * scolta-search as a dependency, which puts it exactly there; registering at
 * top level (not inside a DOMContentLoaded handler) keeps it there.
 */
(function (global) {
  'use strict';

  if (!global.Scolta || typeof global.Scolta.setResultRenderer !== 'function') {
    // A bundle without the render seam is not something to work around here.
    console.warn('[terra-collecta] Scolta.setResultRenderer unavailable; leaving the built-in card in place.');
    return;
  }

  var ENTITIES = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  };

  function escapeHtml(value) {
    return String(value === null || value === undefined ? '' : value)
      .replace(/[&<>"']/g, function (c) { return ENTITIES[c]; });
  }

  /**
   * Escapes a URL for an attribute and neutralizes non-http(s) schemes.
   *
   * The image URL is written into the index as a root-relative path, but it
   * arrives here as raw index data, so it gets the same treatment Scolta gives
   * the result href rather than an assumption about who wrote it.
   */
  function safeImageUrl(value) {
    var url = String(value === null || value === undefined ? '' : value).trim();
    if (url === '') {
      return '';
    }
    if (/^[a-z][a-z0-9+.-]*:/i.test(url) && !/^https?:/i.test(url)) {
      return '';
    }
    return escapeHtml(url);
  }

  /**
   * Drops the thumbnail when its image fails to load.
   *
   * Adding a class rather than removing the node keeps the handler cheap and
   * lets the stylesheet decide what an imageless card looks like.
   */
  global.tcScoltaThumbFailed = function (img) {
    var card = img.closest ? img.closest('.tc-result') : null;
    if (card) {
      card.classList.add('tc-result--thumb-failed');
    }
  };

  global.tcScoltaSaytThumbFailed = function (img) {
    var box = img.closest ? img.closest('.tc-sayt__thumb') : null;
    if (box) {
      box.removeChild(img);
      box.classList.add('tc-sayt__thumb--empty');
    }
  };

  /**
   * The first of a product's categories.
   *
   * meta.product_cat is written by the Scolta plugin as a comma-joined list of
   * term names. Splitting on the comma is safe here and only here, because the
   * plugin is what joined them; anything this file writes itself uses JSON for
   * exactly the reason a joined string is fragile.
   */
  function firstCategory(value) {
    var raw = String(value === null || value === undefined ? '' : value);
    var first = raw.split(',')[0].trim();
    return first === '' || first.toLowerCase() === 'uncategorized' ? '' : first;
  }

  /**
   * The price block.
   *
   * meta.price_display is already formatted to the shop's currency settings by
   * tc_scolta_card_price(), so the browser neither picks a symbol nor rounds:
   * a card and the product page it links to cannot disagree about a price.
   * meta.price_was is present only on a sale, and the old price is struck
   * through beside the new one rather than labelled, which is how the shop
   * writes a sale everywhere else.
   *
   * Nothing in this catalogue is on sale today, so the second half is dormant
   * and correct the day a sale price is set.
   */
  function priceHtml(meta) {
    var now = String(meta.price_display || '').trim();
    if (now === '') {
      return '';
    }
    var was = String(meta.price_was || '').trim();
    return '<span class="tc-result__price">'
      + (was !== '' ? '<s class="tc-result__price-was">' + escapeHtml(was) + '</s> ' : '')
      + '<span class="tc-result__price-now' + (was !== '' ? ' tc-result__price-now--sale' : '') + '">'
      + escapeHtml(now) + '</span>'
      + '</span>';
  }

  /**
   * The stock badge.
   *
   * Only drawn when a product is NOT in stock. Every one of the 1000 products
   * in this catalogue is in stock, so an "In stock" badge would print the same
   * two words on every card in every result list and tell a shopper nothing.
   * Absence of the badge is the signal; its presence is the exception, which
   * is the only version of this badge worth the row space.
   */
  function stockHtml(meta) {
    var status = String(meta.stock_status || '').trim().toLowerCase();
    if (status === '' || status === 'instock') {
      return '';
    }
    var label = status === 'onbackorder' ? 'On backorder' : 'Out of stock';
    return '<span class="tc-result__badge tc-result__badge--oos">' + escapeHtml(label) + '</span>';
  }

  /**
   * Renders one result.
   *
   * Escaping: every ctx value used here ends in Html, Attr or Text, or is
   * safeUrl, so Scolta has already escaped it exactly as its own card would.
   * Everything read from data.meta is raw index data and is escaped here.
   * ctx.query and ctx.highlightTerms are raw and never reach the markup.
   *
   * A product with no featured image gets the same card without the thumbnail,
   * not Scolta's built-in one. Every product in this catalogue has one, so
   * that path is a guard rather than a common case, but mixing two card
   * designs down one result list reads as a broken page and the guard costs a
   * branch.
   */
  global.Scolta.setResultRenderer(function (data, ctx) {
    var meta = (data && data.meta) || {};
    var imageUrl = safeImageUrl(meta.image);
    var alt = escapeHtml(meta.image_alt || '');
    var category = firstCategory(meta.product_cat);

    var metaRow = '<div class="tc-result__meta">'
      + priceHtml(meta)
      + (category !== '' ? '<span class="tc-result__badge">' + escapeHtml(category) + '</span>' : '')
      + stockHtml(meta)
      + '</div>';

    // The thumbnail is decorative: the title link beside it goes to the same
    // product, so it stays out of the tab order and out of the accessible tree.
    var thumb = imageUrl === '' ? ''
      : '<a class="tc-result__thumb" href="' + ctx.safeUrl + '" target="_blank" rel="noopener"'
        + ' tabindex="-1" aria-hidden="true">'
        + '<img src="' + imageUrl + '" alt="' + alt + '" loading="lazy" decoding="async"'
        + ' onerror="tcScoltaThumbFailed(this)">'
        + '</a>';

    // target/rel match the built-in card: within one result list, a card with
    // a thumbnail must not open differently from one without.
    return '<div class="scolta-result-card tc-result">'
      + thumb
      + '<div class="tc-result__body">'
      + '<a class="scolta-result-title tc-result__title" href="' + ctx.safeUrl + '"'
      + ' target="_blank" rel="noopener" title="' + ctx.titleAttr + '">' + ctx.titleHtml + '</a>'
      + metaRow
      + '<div class="scolta-result-excerpt tc-result__excerpt">' + ctx.excerptHtml + '</div>'
      + '</div>'
      + '</div>';
  });

  // Behind its own guard rather than the file-level one: this seam landed
  // after setResultRenderer, so a bundle old enough to lack it still gets the
  // rich cards above, and the dropdown degrades to the themed but imageless
  // rows instead of throwing.
  if (typeof global.Scolta.setSuggestionRenderer !== 'function') {
    return;
  }

  /**
   * Renders one search-as-you-type suggestion row.
   *
   * Returns the row's INNER markup only. The option element around it is the
   * bundle's, and it is what carries the combobox contract — role="option",
   * the stable id the input's aria-activedescendant points at, aria-selected,
   * the data-scolta-sayt-index the keyboard and click handlers dispatch on,
   * and the href in navigate mode. None of that is restated here, because a
   * renderer cannot break by omission what it never writes.
   *
   * The row carries the product photograph and its price. On a shop those are
   * the two facts that decide whether a suggestion is worth following, and a
   * dropdown that shows them is the difference between a list of names and a
   * usable shortcut into the catalogue.
   *
   * Escaping: ctx.titleHtml and ctx.excerptHtml arrive pre-escaped, escaped
   * exactly as the built-in row escapes them. suggestion.meta.* is raw index
   * data and is escaped here. ctx.query is raw and never reaches the markup.
   *
   * A recent search is handed back to the built-in row by returning null: it
   * has no fragment, no image, no price and nothing to add, and the built-in
   * row is already the themed glyph treatment this dropdown wants for history.
   */
  global.Scolta.setSuggestionRenderer(function (suggestion, ctx) {
    if (!suggestion || suggestion.type !== 'title') {
      return null;
    }

    var meta = suggestion.meta || {};
    var imageUrl = safeImageUrl(meta.image);
    var price = String(meta.price_display || '').trim();

    // Decorative, and deliberately not carrying meta.image_alt: an option's
    // accessible name is computed from its contents, so alt text here would be
    // announced in front of the title it illustrates. The title names the row.
    //
    // A row with no image still gets the box, empty and with its border and
    // fill removed, so every title starts on the same line.
    var thumb = imageUrl === ''
      ? '<span class="tc-sayt__thumb tc-sayt__thumb--empty" aria-hidden="true"></span>'
      : '<span class="tc-sayt__thumb" aria-hidden="true">'
        + '<img src="' + imageUrl + '" alt="" loading="lazy" decoding="async"'
        + ' onerror="tcScoltaSaytThumbFailed(this)">'
        + '</span>';

    return '<span class="tc-sayt">'
      + thumb
      // Both classes on purpose. The scolta-* one carries the look the theme
      // already gives a suggestion's title and excerpt, so a title row and a
      // recent-search row stay typographically identical; the tc-* one adds
      // only the layout this row needs. Two classes at the same specificity,
      // resolved by source order, rather than a nested selector.
      + '<span class="tc-sayt__text">'
      + '<span class="scolta-sayt-title tc-sayt__title">' + ctx.titleHtml + '</span>'
      + (ctx.excerptHtml
        ? '<span class="scolta-sayt-excerpt tc-sayt__excerpt">' + ctx.excerptHtml + '</span>'
        : '')
      + '</span>'
      + (price !== '' ? '<span class="tc-sayt__price">' + escapeHtml(price) + '</span>' : '')
      + '</span>';
  });

})(window);
