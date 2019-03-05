const functions = require('firebase-functions');
const admin = require('firebase-admin');

admin.initializeApp(functions.config().firebase);

const studentsRef = admin.firestore().collection('students');
const dashboardRef = admin.firestore().collection('dashboard');

exports.addStudent = functions.firestore
  .document('students/{studentId}')
  .onCreate((snap, context) => {
    var newStudent = snap.data();
    console.log('New student in collection: ', newStudent);
    
    var activeCount = 0;
    studentsRef.where('status', '==', true).stream()
      .on('data', (snap) => {
        ++activeCount;     
      }).on('end', () => { 
          dashboardRef.where('type', '==', 'students').get()
            .then(querySnap => {
              if (querySnap.docs[0].data().count == activeCount){
                console.log('No new active student: ', querySnap.docs[0].data());
              } else {
                console.log('New active counts: ', activeCount);
                console.log('Student Dashboard before update: ', querySnap.docs[0].id, '=>', querySnap.docs[0].data());
                dashboardRef.doc(querySnap.docs[0].id).update({
                  count: activeCount
                });
                console.log('Student count updated: ', querySnap.docs[0].data().count, '=>', activeCount);
              };
            });
        });
  return null
  });
