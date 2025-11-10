import React from "react";
import Back from "../common/back/Back";
import "./contact.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLinkedin, faXTwitter, faInstagram } from "@fortawesome/free-brands-svg-icons";

const Contact = () => {
  const map = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d224611.5987632939!2d77.15425664186684!3d28.402468501787542!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390cdc15f5a424b1%3A0xe4f50576c850e0f2!2sFaridabad%2C%20Haryana!5e0!3m2!1sen!2sin!4v1739636819158!5m2!1sen!2sin';

  return (
    <>
      <Back title='Contact Us' />
      <section className='contacts padding'>
        <div className='container shadow flexSB'>
          <div className='left row'>
            <iframe src={map} title="Google Maps"></iframe>
          </div>
          <div className='right row'>
            <h1>Contact us</h1>
            <p>We're open for any suggestion or just to have a chat</p>

            <div className='items grid2'>
              <div className='box'>
                <h4>ADDRESS:</h4>
                <p>Faridabad, 121001, Haryana, India</p>
              </div>
              <div className='box'>
                <h4>EMAIL:</h4>
                <p>mentalglow-ai@gmail.com</p>
              </div>
              <div className='box'>
                <h4>PHONE:</h4>
                <p>+91 70******31</p>
              </div>
            </div>

            <form action=''>
              <div className='flexSB'>
                <input type='text' placeholder='Name' />
                <input type='email' placeholder='Email' />
              </div>
              <input type='text' placeholder='Subject' />
              <textarea cols='30' rows='10' placeholder="Enter Message"></textarea>
              <button className='primary-btn'>SEND MESSAGE</button>
            </form>

            <h3>Follow us here</h3>
            <div className='social-icons'>
              <i className='icon'><a href="/"><FontAwesomeIcon icon={faLinkedin} /></a></i>
              <i className='icon'><a href="/"><FontAwesomeIcon icon={faXTwitter} /></a></i>
              <i className='icon'><a href="/"><FontAwesomeIcon icon={faInstagram} /></a></i>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default Contact;
