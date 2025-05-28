const currentIndices = {
  {% for level in levels %}
  '{{level.0}}': 0,
  {% endfor %}
};

const places = [
    {% for level in levels %}
    {% for place in level.2 %}
    {% if place.first_img %}
    {
      id: '{{ level.0 }}',
      name: '{{ place.name }}',
      description: '{{ place.description|escapejs }}',
      img: '/media/{{ place.first_img.img }}'
    },
    {% endif %}
    {% endfor %}
    {% endfor %}
  ].filter(p => p.id === levelId);

function updateFloorDisplay(levelId) {
  if (places.length === 0) return;

  const currentIndex = currentIndices[levelId];
  const currentPlace = places[currentIndex % places.length];

  document.getElementById(`${levelId}-main-img`).src = currentPlace.img;
  document.querySelector(`#$level-{levelId} h4`).textContent = currentPlace.name;
  document.querySelector(`#$level-{levelId} p`).textContent = currentPlace.description;
}

function nextImage(levelId) {
  currentIndices[levelId]++;
  updateFloorDisplay(levelId);
}

function prevImage(levelId) {
  currentIndices[levelId]--;
  updateFloorDisplay(levelId);
}