import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
import MyForm from './login'
const App = () => (
  <DataProvider endpoint="tasks/notif/"
                render={data => <Table data={data} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;

const wrapper1 = document.getElementById("login");
wrapper1 ? ReactDOM.render(<MyForm />, wrapper1) : null;

