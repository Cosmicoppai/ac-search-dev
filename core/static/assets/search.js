let value;
let searchButton = document.getElementById('searchButton');
searchButton.addEventListener('click', (event) => {
    event.preventDefault()
    let search = document.getElementById('search').value;
    let subreddits = document.getElementById('subreddits').value;
    // console.log(subreddits)
    if (document.getElementById('filterPost').checked && document.getElementById('filterComment').checked) {
        value = "both"
    }
    else if (document.getElementById('filterPost').checked) {
        value = "posts"
    } else if (document.getElementById('filterComment').checked) {
        value = "comments"
    }
    // console.log(value)
    if (value === 'both') {
        fetch('/search?sub=' + subreddits + '&search=' + search + '&filter1=posts&filter2=comments')
            .then(response => {
                console.log(response)
            })
            .then(data => {
                // console.log(data)
            });
    }
    else if (value === 'posts') {
        fetch('/search?sub=' + subreddits + '&search=' + search + '&filter1=' + value)
            .then(response => {
                console.log(response)
                // return response.json();
            })
            .then(data => {
                // console.log(data)
            });
    }
    else if (value === 'comments') {
        fetch('/search?sub=' + subreddits + '&search=' + search + '&filter2=' + value)
            .then(response => {
                // console.log(response)
            })
            .then(data => {
                // console.log(data)
            });
    }
})

