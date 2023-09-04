
let db = new sqlite3.Database('school.db', (err) => {
    if (err){
        return console.error(err.message);
    }
    console.log('Connected to school database.');
});