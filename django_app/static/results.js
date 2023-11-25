let response = fetch('', {
    method: 'get',
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    },
});

let data = response.json();
console.log(await data);
