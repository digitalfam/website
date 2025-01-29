document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loading-overlay').style.display = 'none';
    
    const scrollContainers = document.querySelectorAll('.overflow-x-scroll');

    scrollContainers.forEach(container => {
        container.addEventListener('wheel', function (event) {
            if (event.deltaY !== 0) {
                event.preventDefault();
                container.scrollLeft += event.deltaY;
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var someElement = document.getElementById("nonExistentElement");
    if (someElement) {
        someElement.style.display = "none";
    }
});