var admin = require("firebase-admin");
var serviceAccount = require("/home/peringer/firebase-query/firebase_key.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://fir-query-3772d.firebaseio.com"
});

var db = admin.database();


var uid = 'Alan'

var usersRef = db.ref(`users/${uid}`);

usersRef.once("value", function(snapshot) {
  val = snapshot.val();
  console.log(val.scores);});
