module.exports = (function() {
    'use strict';

    var mongo = require('mongodb')
    var express = require('express');
    var bodyParser = require('body-parser')
    var schedule_service = require('./schedule_service')
    var service_instance = new schedule_service();
    var router = require('express').Router();

    router.use(bodyParser.json());

    router.get('/classroom', function (req, res) {
      var param = req.query.location;
      var classroom = {
        "lectures.location": param
      }

      service_instance.find_classroom(classroom)
      .then(function(result){
        if(result == null){
          res.status(404).send(result);
        }
        else{
          res.status(200).send(result);
        }
      })
      .catch(function(error){
        console.error(error)
      })
    });

    // router.post('/users/save', function (req, res) {
    //   var first_name = req.body.first_name
    //   var last_name = req.body.last_name
    //   var birth_date = req.body.birth_date
    //   var e_mail = req.body.e_mail
    //   var tc_no = req.body.tc_no
    //   var user_id = req.body.user_id
    //   var user = {
    //     "first_name": first_name,
    //     "last_name": last_name,
    //     "birth_date": birth_date,
    //     "e_mail": e_mail,
    //     "tc_no": tc_no,
    //     "_id": user_id
    //   }
    //
    //   service_instance.insert_user(user)
    //   .then(function(user){
    //     res.status(201).send(user);
    //     console.log('Insert user ' + JSON.stringify(user));
    //   })
    //   .catch(function(error){
    //     console.error(error)
    //     res.status(500).send(error)
    //   })
    // });

    return router;
})();
