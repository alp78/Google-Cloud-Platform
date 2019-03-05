const nodemailer = require('nodemailer');
const sgMail = require('@sendgrid/mail');

exports.sendEmail = (req, res) => {
  var email = req.query.message; // destination email address transmitted as argument in the function call
  
  // Nodemailer config
  var gmailEmail = process.env.EMAIL;
  var gmailPassword = process.env.PASSWORD;
  
  var APP_NAME = 'Email Sender';
  var displayName = 'Mailbot';
  
  var mailTransport = nodemailer.createTransport({
    service: 'Gmail',
    auth: {
      user: gmailEmail,
      pass: gmailPassword
    }
  });
  
  var mailOptions = {
    from: gmailEmail,
    to: email,
    subject: 'Nodemailer',
    text: 'Sent with Nodemailer'  
  };
  
  mailTransport.sendMail(mailOptions);
  
  // Sendgrid config
  
  sgMail.setApiKey(process.env.GRIDKEY);
  var msg = {
    to: email,
    from: gmailEmail,
    subject: 'Sendgrid',
    text: 'Sent with Sendgrid/mail'
  };
  
  sgMail.send(msg);
  
  return `Sent mail with Sendgrid and Nodemailer`;
  
};
