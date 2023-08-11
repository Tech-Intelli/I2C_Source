import React, { useRef, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { Circles } from "react-loader-spinner";
import "./UploadFile.css";
import Navbar from "../Navbar/Navbar";

const apiKey = `${process.env.REACT_APP_MAP_API}`;
const mapApiJs = 'https://maps.googleapis.com/maps/api/js';

function loadAsyncScript(src) {
  return new Promise((resolve) => {
    const script = document.createElement("script");
    Object.assign(script, {
      type: "text/javascript",
      async: true,
      src,
    });
    script.addEventListener("load", () => resolve(script));
    document.head.appendChild(script);
  });
}

const extractAddress = (place) => {
  const address = {
    city: "",
    country: "",
    plain() {
      const city = this.city ? this.city + ", " : "";
      return city + this.country;
    },
  };

  if (!Array.isArray(place?.address_components)) {
    return address;
  }

  place.address_components.forEach((component) => {
    const types = component.types;
    const value = component.long_name;

    if (types.includes("locality")) {
      address.city = value;
    }

    if (types.includes("country")) {
      address.country = value;
    }
  });

  return address;
};

export const UploadFile = (props) => {
  const token = localStorage.getItem("token");
  const inputRef = useRef();
  const navigate = useNavigate();
  const wrapperRef = useRef();
  const searchInput = useRef(null);
  const [fileList, setFileList] = useState();
  const [file, setFile] = useState();
  const [fileType, setFileType] = useState();
  const [loading, setLoading] = useState(false);
  const [memory, setMemory] = useState("");
  const [address, setAddress] = useState({});
  const [errorMessage, setErrorMessage] = useState("");

  const onDragEnter = () => wrapperRef.current.classList.add("dragover");
  const onDragLeave = () => wrapperRef.current.classList.remove("dragover");
  const onDrop = () => wrapperRef.current.classList.remove("dragover");

  const onFileDrop = (e) => {
    const newFile = e.target.files[0];
    const input_file = e.target.files[0];
    setFileList(input_file);
    setFileType(newFile.type.split("/")[1]);
    setFile(URL.createObjectURL(e.target.files[0]));
  };

  const fileRemove = () => {
    setFile();
    setFileList();
  };

  // init gmap script
  /*const initMapScript = () => {
    // if script already loaded
    if (window.google) {
      return Promise.resolve();
    }
    const src = `${mapApiJs}?key=${apiKey}&libraries=places&v=weekly`;
    return loadAsyncScript(src);
  };*/

  // do something on address change
  const onChangeAddress = (autocomplete) => {
    const place = autocomplete.getPlace();
    setAddress(extractAddress(place));
  };

  // init autocomplete
  
  const initAutocomplete = () => {
    if (!searchInput.current) return;

    const autocomplete = new window.google.maps.places.Autocomplete(
      searchInput.current
    );
    autocomplete.setFields(["address_component", "geometry"]);
    autocomplete.addListener("place_changed", () =>
      onChangeAddress(autocomplete)
    );
  };
  const initMapAndAutocomplete = () => {
    initAutocomplete();
  };

  // load map script after mounted
  useEffect(() => {
    if (window.google) {
      initMapAndAutocomplete();
    } else {
      const script = document.createElement("script");
      script.src = `${mapApiJs}?key=${apiKey}&libraries=places&v=weekly&callback=Function.prototype`;
      script.onload = initMapAndAutocomplete;
      script.onerror = (error) => {
        console.error("Error loading Google Maps API:", error);
      };
      document.head.appendChild(script);
    }
  }, []);


  const validateForm = () => {
    if (!file) {
      setErrorMessage("*Please upload an image or video before proceeding.");
      return false;
    }
    return true;
  };

  const handleClick = () => {
    setLoading(true);
    setErrorMessage("");
    if (!validateForm()) {
      setLoading(false);
      return;
    }
    const formData = new FormData();
    formData.append("file", fileList);
    if (address) {
      formData.append("address", JSON.stringify(address));
    }
    axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/upload_file`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true,
      })
      .then((res) => {
        const file = res.data.file_name;
        const address = res.data.address;
        setLoading(false);
        navigate("/generatecaption", { state: { memory, file, address} });
      })
      .catch((err) => {
        console.log("Error", err);
      });
  };

  return (
    <>
      <div>

        <Navbar flag={true}/>
        <section>
          <div className="content-page1">
            <div className="innerContent-page1">
              <p className="steps">Upload Files</p>
              <div className="context-location-container">
                <div>
                  <p className="label">Something about your memory:</p>
                  <input
                    type="text"
                    placeholder="Memory (optional)..."
                    className="inputs context-page1"
                    value={memory}
                    onChange={(e) => setMemory(e.target.value)}
                  ></input>
                </div>
                <div>
                  <p className="label">Add Location:</p>
                  <div className="search">
                    <input
                      ref={searchInput}
                      type="text"
                      placeholder="Search location...."
                      className="inputs location"
                    />
                  </div>
                </div>
              </div>
              <div
                ref={wrapperRef}
                className="drop-file-input"
                onDragEnter={onDragEnter}
                onDragLeave={onDragLeave}
                onDrop={onDrop}
              >
                <div className="drop-file-input__label">
                  {!file ? (
                    <>
                      <i
                        className="fa-regular fa-image"
                        style={{ color: "#989aa0" }}
                      ></i>
                      <p className="title">
                        Add Photo or Video <span style={{ color: "red" }}>*</span>
                      </p>
                      <p className="subtitle">Drag & Drop your files here</p>
                    </>
                  ) : fileType === "mp4" || fileType === "mov" || fileType === "quicktime" ? (
                    <video controls className="selectedFile">
                      <source src={file}></source>
                    </video>
                  ) : (
                    <img src={file} className="selectedFile" alt="Preview" />
                  )}
                </div>
                {file && (
                    <button className="removeBtn" onClick={fileRemove}>
                      <i className="fas fa-times"></i>
                    </button>
                  )}
                {!file ? (
                  <input
                    ref={inputRef}
                    accept="image/jpg,image/png,image/jpeg,video/mp4,video/quicktime"
                    type="file"
                    value=""
                    onChange={(e) => onFileDrop(e)}
                  />
                ) : null}
              </div>
              <div style={{ display: "flex", flexDirection: "column", alignItems:"center"  }}>
                {errorMessage && <p className="error-message">{errorMessage}</p>}
                {loading ? (
                  <div className="spinners">
                    <Circles
                      height="50"
                      width="50"
                      color="var(--font-col)"
                      ariaLabel="circles-loading"
                      wrapperStyle={{}}
                      wrapperClass=""
                      visible={true}
                    ></Circles>
                    <p className="load-message">Uploading the file....</p>
                  </div>
                ) : (
                  <button className="btn-style-page1" onClick={handleClick}>
                    <span>Next</span>
                  </button>
                )}
              </div>
            </div>
          </div>

          <div className="footer-page1"></div>
        </section>
      </div>
    </>
  );
};
