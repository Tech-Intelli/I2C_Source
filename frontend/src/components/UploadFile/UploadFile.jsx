import React, { useRef, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { Circles } from "react-loader-spinner";
import "./UploadFile.css";
const apiKey = process.env.REACT_APP_MAP_API;
const mapApiJs = 'https://maps.googleapis.com/maps/api/js';

function loadAsyncScript(src) {
  return new Promise(resolve => {
    const script = document.createElement("script");
    Object.assign(script, {
      type: "text/javascript",
      async: true,
      src
    })
    script.addEventListener("load", () => resolve(script));
    document.head.appendChild(script);
  })
}

const extractAddress = (place) => {

  const address = {
    city: "",
    country: "",
    plain() {
      const city = this.city ? this.city + ", " : "";
      return city + this.country;
    }
  }

  if (!Array.isArray(place?.address_components)) {
    return address;
  }

  place.address_components.forEach(component => {
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
}



export const UploadFile = (props) => {
  const token = localStorage.getItem("token");
  const inputref = useRef();
  const navigate = useNavigate();
  const wrapperRef = useRef();
  const [fileList, setFileList] = useState();
  const [file, setfile] = useState();
  const [fileType, setFileType] = useState();
  const [loading,setLoading] = useState(false);
  const onDragEnter = () => wrapperRef.current.classList.add("dragover");
  const onDragLeave = () => wrapperRef.current.classList.remove("dragover");
  const onDrop = () => wrapperRef.current.classList.remove("dragover");
  
  const [memory,setMemory] = useState(''); //memory is used to access the memory context

  const onFileDrop = (e) => {
    const newFile = e.target.files[0];
    const input_file = e.target.files[0];
    setFileList(input_file);
    setFileType(newFile.type.split("/")[1]);
    setfile(URL.createObjectURL(e.target.files[0]));
  };

  const fileRemove = () => {
    setfile();
    setFileList();
  };
  const searchInput = useRef(null);
  const [address, setAddress] = useState({});
 

  // init gmap script
  const initMapScript = () => {
    // if script already loaded
    if(window.google) {
      return Promise.resolve();
    }
    const src = `${mapApiJs}?key=${apiKey}&libraries=places&v=weekly`;
    return loadAsyncScript(src);
  }

  // do something on address change
  const onChangeAddress = (autocomplete) => {
    const place = autocomplete.getPlace();
    setAddress(extractAddress(place));
  }

  // init autocomplete
  const initAutocomplete = () => {
    if (!searchInput.current) return;

    const autocomplete = new window.google.maps.places.Autocomplete(searchInput.current);
    autocomplete.setFields(["address_component", "geometry"]);
    autocomplete.addListener("place_changed", () => onChangeAddress(autocomplete));

  }
  // load map script after mounted
  useEffect(() => {
    initMapScript().then(() => initAutocomplete())
  }, []);

  const handleClick = () => {
    setLoading(true);
     const formData = new FormData();
     formData.append("file", fileList);
     if (address) {
      formData.append("address", JSON.stringify(address));
    }
    console.log(JSON.stringify(address));
     axios
      .post(
        "http://localhost:9000/upload_file",formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": 'multipart/form-data',
          },
          withCredentials: true,
        }
      )
      .then((res) => {
        setLoading(false);
        navigate("/generatecaption", {state: { memory }});
      })
      .catch((err) => {
        console.log("Error", err);
      });
  };

  const [showDropdown, setShowDropdown] = useState(false); // To convert the user icon into dropdown
  const toggleDropdown = () => {
    console.log("User was clicked");
    setShowDropdown(!showDropdown);
  };
  const handleLogout = async() => {
    await axios.post("http://localhost:9000/logout_user")
    .then((res)=>{
      navigate("/");
    })
    .catch((err) => {
      console.log("Error", err);
    });
    console.log("Go to Login")
  };

  return (
    <>
      <div>
        <div className="header-page1">
          <div>
            <p>ExplAIstic</p>
          </div>
          <div className="icons-page1">
            <i
                className={`fa-regular fa-user ${showDropdown ? 'active' : ''}`}
                onClick={toggleDropdown}
              ></i>
            <i className="fa-solid fa-bars"></i>
          </div>
        </div>
        <section>
          <div className="content-page1">
          {showDropdown && (
            <div className="dropdown-input">
              <ul>
                <li onClick={handleLogout}>Log out</li>
              </ul>
            </div>
          )}
            <div className="innerContent-page1">
            
              <p className="steps">Step 1 :Upload Files</p>
              <div className="context-location-container">
                <div>
                  <p className="label">
                    Something about your memory:
                  </p>
                  <input
                    type = "text"
                    placeholder="Memory (optional)..."
                    className="inputs context-page1"
                    value={memory}
                    onChange={(e) => setMemory(e.target.value)}
                  ></input>
                </div>
                <div>
                  <p className="label">
                    Add Location:
                  </p>
                  <div className="search">
                      <input ref={searchInput} type="text" placeholder="Search location...." className="inputs location"/>
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
                        class="fa-regular fa-image"
                        style={{ color: "#989aa0" }}
                      ></i>
                      <p className="title">
                        Add Photo or Video{" "}
                        <span style={{ color: "red" }}>*</span>
                      </p>
                      <p className="subtitle">Drag & Drop your files here</p>
                    </>
                  ) : (fileType === "mp4" || fileType === "mov" || fileType === "quicktime") ? (
                    <video controls className="selectedFile">
                      <source src={file}></source>
                    </video>
                  ) : (
                    <img src={file} className="selectedFile"></img>
                  )}
                </div>
                {!file ? (
                  <input
                    ref={inputref}
                    accept="image/jpg,image/png,image/jpeg,video/mp4,video/quicktime"
                    type="file"
                    value=""
                    onChange={(e) => onFileDrop(e)}
                  />
                ) : null}
              </div>
              <div style={{ display: "flex", flexDirection: "column" }}>
                {file ? (
                  <button className="deleteBtn" onClick={fileRemove}>
                    Remove File
                  </button>
                ) : null}

                {loading? <>
                  <div className="spinners">
                    <Circles
                      height="50"
                      width="50"
                      color="#1c4042"
                      ariaLabel="circles-loading"
                      wrapperStyle={{}}
                      wrapperClass=""
                      visible={true}
                    ></Circles>
                  </div>
                </>:<button className="btn-style-page1" onClick={handleClick}>
                  Next
                </button>}
              </div>
              
            </div>
          </div>

          <div className="footer-page1">
          </div>
        </section>
        <div className="images-page1">
        
        </div>
      </div>
    </>
  );
};
