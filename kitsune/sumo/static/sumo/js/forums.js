import KBox from "sumo/js/kbox";
import AjaxPreview from "sumo/js/ajaxpreview";
import Marky from "sumo/js/markup";

/*
 * forums.js
 * Scripts for the forums app.
 */

(function($) {

  function init() {
    Marky.createSimpleToolbar(
      '.editor-tools',
      '#reply-content, #id_content',
      {mediaButton: true});

    new AjaxPreview($('#preview'));

    $('.post-action a.reply').click(function() {
      var post = $(this).data('post'),
        $post = $('#post-' + post),
        text = $post.find('div.content-raw').text(),
        user = $post.find('.display-name').text(),
        reply_text = `''${user} [[#post-${post}|${gettext('said')}]]''\n<blockquote>\n${text}\n</blockquote>\n\n`,
        $textarea = $('#id_content'),
        oldtext = $textarea.val();

      $textarea.val(oldtext + reply_text);
      return true;
    });
    watchDiscussion();
  }
  function watchDiscussion() {
    // For a thread on the all discussions for a locale.
    $('.watch-form').click(function() {
      var form = $(this);
      $.post(form.attr('action'), form.serialize(), function() {
        form.find('a').toggleClass('yes').toggleClass('no');
        form.find('a.no').attr('title', gettext('You are not watching this thread'));
        form.find('a.yes').attr('title', gettext('You are watching this thread'));
      }).error(function() {
        // error growl
      });
      return false;
    });

  }

  // Lightbox for all images on click
  $('.wiki-image').each(function() {
    var $this = $(this);

    // If the image is already linked do not do this
    if ($this.parents('a').length === 0) {
      $this.on('click', function(ev) {
        ev.preventDefault();
        var imgUrl = $this.attr('src'),
          image = new Image(),
          html = '<div><img class="loading" /></div>',
          kbox = new KBox(html, {
            modal: true,
            title: gettext('Image Attachment'),
            id: 'wiki-image-kbox',
            destroy: true
          });
        kbox.open();

        function setWidth() {
          $('#wiki-image-kbox').width(image.width)
          .find('img').removeClass('loading').attr('src', imgUrl);
          kbox.setPosition();
        }

        image.onload = setWidth;
        image.src = imgUrl;
        if (image.width) {
          setWidth();
        }
      });
    }
  });

  $(document).ready(init);

})(jQuery);
