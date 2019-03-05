const Firestore = require('@google-cloud/firestore');

const db = new Firestore({
  projectId: 'fir-query-3772d',
  keyFilename: '/home/peringer/firebase-query/fir-query-3772d-97aa677ea4ee.json',
});

var usersRef = db.collection('users');

usersRef.get()
  .then((snapshot) => {
    snapshot.forEach((doc) => {
      console.log(doc.id, '=>', doc.data());
    });
  })
  .catch((err) => {
    console.log('Error getting documents', err);
  });