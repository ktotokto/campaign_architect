document.addEventListener('DOMContentLoaded', function() {
  const tabButtons = document.querySelectorAll('.tab-btn');

  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

      button.classList.add('active');
      const tabId = button.getAttribute('data-tab');
      document.getElementById(tabId).classList.add('active');
    });
  });

  const notesTextarea = document.querySelector('.campaign-notes');
  if (notesTextarea) {
    function adjustHeight() {
      notesTextarea.style.height = 'auto';
      notesTextarea.style.height = notesTextarea.scrollHeight + 'px';
    }

    notesTextarea.addEventListener('input', adjustHeight);
    adjustHeight();
  }
});