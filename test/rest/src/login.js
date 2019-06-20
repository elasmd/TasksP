import React, { Component } from "react";
import axios from 'axios';
class MyForm extends Component {
    state = {
      data: [],
      loaded: false,
      placeholder: "Loading..."
    };
  constructor() {
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);
        var username = null;
        var password = null;
    for (var [key, value] of data.entries()) {
        if (key === 'username') username=value;
        else password=value;}
    var postdata = {
        'username':username,
        'password':password
    };
    axios.post('/login/',postdata
    )
        .then(data => {
            console.log(data);
        console.log(data.data);
        return data;
  })
  };

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label htmlFor="username">Enter username</label>
        <input id="username" name="username" type="text" />
        <label htmlFor="password">Enter your password</label>
        <input id="password" name="password" type="password" />
        <button>Send data!</button>
      </form>
    );
  }}
export default MyForm;