import axios from "axios";

import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState([]);
  const [sortedData, setSortedData] = useState([]);
  const [sortColumn, setSortColumn] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  // Sorting function
  const sortData = (column) => {
    const sorted = [...sortedData].sort((a, b) => {
      if (a[column] < b[column]) return sortOrder === "asc" ? -1 : 1;
      if (a[column] > b[column]) return sortOrder === "asc" ? 1 : -1;
      return 0;
    });
    setSortedData(sorted);
  };

  // Handle column header click to change sorting
  const handleSort = (column) => {
    if (column === sortColumn) {
      // Toggle sorting order if same column clicked
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      // Set new sort column and reset order to ascending
      setSortColumn(column);
      setSortOrder("asc");
    }
    // Sort the data
    sortData(column);
  };

  const onFileChange = (event) => {
    // Update the state
    setSelectedFile(Array.prototype.slice.call(event.target.files));
  };

  const onFileUpload = () => {

    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    selectedFile.map((file) => formData.append(`files`, file, file.name));


    // Request made to the backend api
    // Send formData object
    axios
      .post("http://192.168.64.2:8080/uploadfile", formData)
      .then(function (response) {
        const data = response.data;
        
        setSortedData(data);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  const fileResults = () => {
    if (sortedData.length > 0) {
      return (
        <div>
          <h2>Results Table:</h2>

          <div
            style={{ maxHeight: 300, border: "1px solid", overflow: "auto" }}
          >
            <table>
              <thead>
                <tr>
                  <th onClick={() => handleSort(0)}>Date</th>
                  <th onClick={() => handleSort(1)}>Amount</th>
                  <th onClick={() => handleSort(2)}>Description</th>
                  <th onClick={() => handleSort(3)}>Category</th>
                </tr>
              </thead>
              <tbody>
                {sortedData.map((item, index) => (
                  <tr key={index}>
                    <td>{item[0]}</td>
                    <td>{item[1]}</td>
                    <td>{item[2]}</td>
                    <td>{item[3]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      );
    }
  };

  const fileData = () => {
    if (selectedFile.length > 0) {
      return (
        selectedFile.map((file, index) =>(
          <div key={index}>
            <h2>File Details:</h2>

            <p>File Name: {file.name}</p>

            <p>File Type: {file.type}</p>

            <p>Last Modified: {file.lastModifiedDate.toDateString()}</p>
        </div>
        ))
      );
    } else {
      return (
        <div>
          <br />
          <h4>Choose before Pressing the Upload button</h4>
        </div>
      );
    }
  };

  return (
    <div>
      <h3>File Upload using React!</h3>
      <div>
        <input type="file" onChange={onFileChange} multiple/>
        <button onClick={onFileUpload}>Upload!</button>
      </div>
      <section>{fileResults()}</section>
    </div>
  );
}

export default App;
