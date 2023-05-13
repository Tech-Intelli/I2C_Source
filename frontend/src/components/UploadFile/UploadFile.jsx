import React ,{useRef,useState} from "react";
import { Link, useNavigate } from "react-router-dom";


import "./UploadFile.css"

export const UploadFile = (props)=>{
    const navigate = useNavigate();
    const wrapperRef = useRef(null);
    const [fileList, setFileList] = useState();
    const [file,setfile] =useState();
    const [fileType,setFileType] = useState();
    const onDragEnter = () => wrapperRef.current.classList.add('dragover');
    const onDragLeave = () => wrapperRef.current.classList.remove('dragover');
    const onDrop = () => wrapperRef.current.classList.remove('dragover');
    const onFileDrop = (e) => {
        const newFile = e.target.files[0];
        const type = newFile.type.split("/")[1];
        console.log(newFile.type.split("/")[1]);
        setFileType(newFile.type.split("/")[1]);
        setfile(URL.createObjectURL(e.target.files[0]));
        
    }

    const fileRemove = () => {
        setfile();
    }

    const handleClick = () =>{
       navigate("/generatecaption")
    }
    return (


        <>
    <div>
        <div className="header-page1">
            <div>
                <p>ExplAIstic</p>
            </div>
            <div className= "icons-page1">
                <i className="fa-regular fa-user"></i>
                <i className="fa-solid fa-bars"></i>
            </div>
        </div>
        <section>
        <div className="content-page1">
            <div className="innerContent-page1">
            
                <p className="steps">Step 1 :Upload Files</p>
                <div>
                    <p className="label">Add Context <span>(optional)</span></p>
                    <input placeholder="Tell us something about your memory" className="context-page1"></input>
                   
                </div>
                
            
            <div
                ref={wrapperRef}
                className="drop-file-input"
                onDragEnter={onDragEnter}
                onDragLeave={onDragLeave}
                onDrop={onDrop}
            >
                <div className="drop-file-input__label">
                {!file?<><i class="fa-regular fa-image" style={{color: "#989aa0"}}></i> 
                <p className="title">Add Photo or Video <span style={{color:"red"}}>*</span></p>                   
                <p className="subtitle">Drag & Drop your files here</p></>:fileType == 'mp4'|'mov' ? <video controls className="selectedFile"><source src={file}></source></video>:<img src={file} className = "selectedFile"></img>}
                </div>
                {!file?<input accept="image/jpg,image/png,image/jpeg,video/mp4,video/mov" type="file" value="" onChange={onFileDrop}/>:null}
            </div>
            <div style={{display:"flex",flexDirection:"column"}}>
            {file?<button className="deleteBtn" onClick={fileRemove}>Remove File</button>:null}
            <button className="btn-style-page1" onClick={handleClick}>Next</button>
            </div>
        
                
           </div>
       

        </div>
        
        <div className="footer-page1">
            
        </div>
        </section>
    </div>
   
    </>
    )
}