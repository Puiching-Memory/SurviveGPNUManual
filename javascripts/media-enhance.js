/*
  自动增强图片呈现（合并版）：
  - 懒加载 loading=lazy 与 decoding=async
  - 为未包裹链接的图片创建 GLightbox 链接
  - 对已包裹且指向图片的链接追加 glightbox 属性（不改动指向非图片的链接）
  - 跳过表格内图片，避免破坏布局
  - 适配 MkDocs Material 的 SPA 导航（window.document$）+ 兜底事件
  - 幂等执行（重复导航不重复包装）
*/
(function () {
  function isImageUrl(url) {
    return /\.(png|jpe?g|webp|gif|svg)([?#].*)?$/i.test(url || '');
  }

  function enhanceImages(root) {
    var scope = root || document.querySelector('.md-content .md-typeset') || document;
    var imgs = scope.querySelectorAll('img');
    imgs.forEach(function (img) {
      // 幂等：已处理过的图片跳过
      if (img.dataset.enhanced === '1') return;

      // 懒加载与解码优化
      if (!img.hasAttribute('loading')) img.setAttribute('loading', 'lazy');
      if (!img.hasAttribute('decoding')) img.setAttribute('decoding', 'async');

      // 表格内图片不处理（避免灯箱影响表格交互与布局）
      if (img.closest('table')) {
        img.dataset.enhanced = '1';
        return;
      }

      var src = img.currentSrc || img.getAttribute('src') || '';
      // 没有可用 src 或非常见图片格式，直接标记已处理
      if (!src) {
        img.dataset.enhanced = '1';
        return;
      }

      var parentLink = img.closest('a');
      if (parentLink) {
        // 若已有链接，且链接本身指向图片，则增强为灯箱
        var href = parentLink.getAttribute('href') || '';
        if (isImageUrl(href)) {
          parentLink.classList.add('glightbox');
          parentLink.setAttribute('data-type', 'image');
          parentLink.setAttribute('data-gallery', 'page-images');
          var altText = img.getAttribute('alt');
          if (altText && !parentLink.getAttribute('data-title')) {
            parentLink.setAttribute('data-title', altText);
          }
        }
        // 若已有链接但指向非图片（例如跳转到文章或外链），则保留原行为不处理
        img.dataset.enhanced = '1';
        return;
      }

      // 未包裹链接且是图片资源，包装为灯箱链接
      if (isImageUrl(src)) {
        var a = document.createElement('a');
        a.href = src;
        a.className = 'glightbox';
        a.setAttribute('data-type', 'image');
        a.setAttribute('data-gallery', 'page-images');
        var alt = img.getAttribute('alt');
        if (alt) a.setAttribute('data-title', alt);

        var parent = img.parentNode;
        if (parent) {
          parent.insertBefore(a, img);
          a.appendChild(img);
        }
      }

      img.dataset.enhanced = '1';
    });
  }

  function run() {
    enhanceImages();
  }

  // 支持 MkDocs Material SPA 导航
  if (window && window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(run);
  } else {
    document.addEventListener('DOMContentLoaded', run);
    window.addEventListener('load', run);
    // 兼容旧自定义事件（若站点有发出）
    document.addEventListener('DOMContentSwitch', run);
  }
})();
