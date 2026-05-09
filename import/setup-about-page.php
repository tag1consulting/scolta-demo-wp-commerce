<?php
/**
 * Updates the "About Terra Collecta" page with complete demo/Tag1/Scolta context.
 * Run with: wp eval-file /var/www/html/import/setup-about-page.php
 * Idempotent: checks for a sentinel meta key before updating.
 */

$page = get_page_by_path('about-terra-collecta', OBJECT, 'page');

if (! $page) {
    echo "ERROR: about-terra-collecta page not found — was the DB imported?\n";
    return;
}

if (get_post_meta($page->ID, '_scolta_about_updated', true) === '1') {
    echo "About page already updated — skipping.\n";
    return;
}

$content = <<<'HTML'
<h2>About This Site</h2>
<p><strong>Terra Collecta is a fictional geological specimen shop.</strong> It was created by Tag1 Consulting to demonstrate the capabilities of Scolta, an open-source AI-powered search platform, on a WordPress 6.9 e-commerce site powered by WooCommerce.</p>

<h2>What You Are Looking At</h2>
<p>This site is a WordPress 6.9 + WooCommerce demonstration built to show how Scolta performs on a product catalog. The store contains approximately 1,000 geological specimen listings including minerals, crystals, fossils, meteorites, and other collectible earth science objects. Each product includes detailed descriptions, formation information, and provenance notes — making it a rich test of Scolta's ability to handle specialized vocabulary.</p>

<h2>What Scolta Does Here</h2>
<p>The search bar uses Scolta to let you explore the product catalog using natural language rather than category browsing. Try these example queries:</p>
<ul>
  <li>"purple crystals under $50"</li>
  <li>"dinosaur fossils from the Jurassic period"</li>
  <li>"meteorites and space rocks"</li>
  <li>"fluorescent minerals"</li>
  <li>"oldest specimen you have"</li>
</ul>
<p>Scolta uses Pagefind for full-text indexing, Claude via the Anthropic API for query expansion and AI-generated overviews, and a custom BM25-based scoring layer that understands the geological and commercial vocabulary of specimen collecting.</p>

<h2>About Tag1 Consulting</h2>
<p>Tag1 Consulting is one of the leading Drupal development and consulting firms in the world. Tag1 built and open-sources Scolta as a demonstration of what AI-augmented content discovery can look like on modern web platforms. For more information about Tag1 and Scolta, visit <a href="https://tag1.com">tag1.com</a>.</p>

<h2>Reuse and Attribution</h2>
<p>If you are evaluating Scolta for your organization and have questions about how this demo was built or how to implement Scolta for your use case, contact Tag1 Consulting.</p>
HTML;

wp_update_post([
    'ID'           => $page->ID,
    'post_content' => $content,
    'post_title'   => 'About Terra Collecta',
]);

update_post_meta($page->ID, '_scolta_about_updated', '1');

echo "Updated 'About Terra Collecta' page (ID: {$page->ID})\n";
