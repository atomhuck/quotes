document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('faculty-search');
  const list = document.getElementById('faculty-suggestions');
  const container = document.querySelector('#faculty-search').closest('.search-container');

  input.addEventListener('input', function () {
    const query = input.value.trim();

    if (query.length < 2) {
      list.innerHTML = '';
      list.style.display = 'none';
      return;
    }

    fetch(`/search_faculties/?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        list.innerHTML = '';
        if (!data.length) {
          list.style.display = 'none';
          return;
        }

        data.forEach(fac => {
          const li = document.createElement('li');
          const link = document.createElement('a');
          link.href = `/faculties/${fac.slug}/`;
          link.textContent = fac.name;
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

  // Скрыть список при клике вне поля
  document.addEventListener('click', function (e) {
    if (!container.contains(e.target)) {
      list.innerHTML = '';
      list.style.display = 'none';
    }
  });
});