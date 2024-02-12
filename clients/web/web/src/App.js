import axios from "axios";

import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
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
    setSelectedFile(event.target.files[0]);
  };
  const onFileUpload = () => {
    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append("myFile", selectedFile, selectedFile.name);

    // Request made to the backend api
    // Send formData object
    axios
      .post("http://192.168.64.2:8080/uploadfile", formData)
      .then(function (response) {
        setSortedData(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  };
  const fileResults = () => {
    if (sortedData) {
      return (
        <div>
          <h2>Results Table:</h2>

          <div
            style={{ maxHeight: 300, border: "1px solid", overflow: "auto" }}
          >
            <table>
              <thead>
                <tr>
                  <th onClick={() => handleSort("Date")}>Date</th>
                  <th onClick={() => handleSort("Amount")}>Amount</th>
                  <th onClick={() => handleSort("Description")}>Description</th>
                  <th onClick={() => handleSort("Category")}>Category</th>
                </tr>
              </thead>
              <tbody>
                {sortedData.map((item, index) => (
                  <tr key={index}>
                    <td>{item.Date}</td>
                    <td>{item.Amount}</td>
                    <td>{item.Description}</td>
                    <td>{item.Category}</td>
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
    if (selectedFile) {
      return (
        <div>
          <h2>File Details:</h2>

          <p>File Name: {selectedFile.name}</p>

          <p>File Type: {selectedFile.type}</p>

          <p>Last Modified: {selectedFile.lastModifiedDate.toDateString()}</p>
        </div>
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
        <input type="file" onChange={onFileChange} />
        <button onClick={onFileUpload}>Upload!</button>
      </div>
      <section>{fileData()}</section>
      <section>{fileResults()}</section>
    </div>
  );
}

export default App;
