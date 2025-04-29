document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('prof-search');
  const list = document.getElementById('suggestions');
  const container = document.querySelector('.search-container');

  input.addEventListener('input', function () {
    const query = input.value.trim();

    if (query.length < 2) {
      list.innerHTML = '';
      list.style.display = 'none';
      return;
    }

    fetch(`/search/?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        list.innerHTML = '';
        if (!data.length) {
          list.style.display = 'none';
          return;
        }

        data.forEach(prof => {
          const li = document.createElement('li');
          const link = document.createElement('a');
          link.href = `/professors/${prof.slug}/`;
          link.textContent = prof.name;
          li.appendChild(link);
          list.appendChild(li);
        });

        list.style.display = 'block';
      })
      .catch(() => {
        list.innerHTML = '';
        list.style.display = 'none';
      });
  });

  // Скрытие подсказок при клике вне поля
  document.addEventListener('click', function (e) {
    if (!container.contains(e.target)) {
      list.innerHTML = '';
      list.style.display = 'none';
    }
  });
});