import React from 'react';
import "./card.css";

import image from "./image.jpeg";
//import logo from "./logo.jpg";

const Card = (props) => {
    const relativePath = props.path.split('/public/')[1];
    const fileExtension = relativePath.split('.').pop().toLowerCase();
    const fileType = fileExtension === 'mp4' || fileExtension === 'mov' || fileExtension === 'quicktime'
        ? 'video'
        : 'image';

    return (
        <div className="card-page">
            {/* Rest of the code */}
            <div className="imgBx">
                {fileType === "video" ? (
                    <video controls className="cover">
                        <source src={`${process.env.PUBLIC_URL}/${relativePath}`}></source>
                    </video>
                ) : (
                    <img src={`${process.env.PUBLIC_URL}/${relativePath}`} alt="" className='cover' />
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