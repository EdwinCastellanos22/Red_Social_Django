const toggleComments = (post_id) => {
    var comments = document.getElementById(`c_${post_id}`);
    comments.classList.toggle('hidden');

    var toggleButton = document.getElementById(`toogle_${post_id}`);
        if (comments.classList.contains('hidden')) {
            toggleButton.innerText = 'Mostrar comentarios';
        } else {
            toggleButton.innerText = 'Ocultar comentarios';
    }
}