import React from 'react'
import "./card.css";

import image from "./image.jpeg";
//import logo from "./logo.jpg";

const Card = (props) => {
    const relativePath = props.path.split('/public/')[1];
  return (
    <div className="card-page">
        <div className="top">
            <div className="userDetails">
                <div className="profile_img">
                    <img src ="" class = "cover"/>
                </div>
                <h3>User_Name<br/><span>India</span></h3>
            </div>
            <div>
                <i class="fa-solid fa-ellipsis-vertical dot"></i>
            </div>
        </div>
        <div className="imgBx">
            {(fileType === "mp4" || fileType === "mov" || fileType === "quicktime")? (
                <video controls className="cover">
                    <source src={`${process.env.PUBLIC_URL}/${relativePath}`} ></source>
                </video>
                ) : (
                <img src={`${process.env.PUBLIC_URL}/${relativePath}`} alt="" className='cover'/>
            )}
            
        </div>
        <div className='actionBtns'>
            <div className="left">
                <i class="fa-regular fa-heart"></i>
                <i class="fa-regular fa-comment"></i>
                <i class="fa-solid fa-share"></i>
            </div>
            <div className="right">
            <i class="fa-regular fa-bookmark"></i>
            </div>
        </div>
        <h4 className='likes'></h4>
        <h4 className='message'><span></span></h4>

    </div>
  )
}

export default Card