
import './App.css'
import { v4 as uuid } from 'uuid';
import { useState } from 'react';
import { useEffect } from 'react';
import IntroComponent from './components/TypingEffect'
import LinkedInIcon from './components/linkedinLogo.jsx';
import GithubIcon from './components/githubLogo.jsx';

function App() {
  const [isUploading, setIsUploading] = useState(false);
  const [keyFile, setKeyFile] = useState(null);
  const [templateFile, setTemplateFile] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [downloadURL, setDownloadURL] = useState(null);

  useEffect(() => {
    // console.log('useEffect is firing')
    const newUserID = uuid();

    if (!sessionStorage.getItem('userID')) {
      sessionStorage.setItem('userID', newUserID);
      console.log("Assigned UUID: ", newUserID);
    } else {
      console.log('Existing UUID: ', sessionStorage.getItem('userID'));
    }
  }, []);

  function handleTemplateFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    const fileName = file.name.toLowerCase();
    if (fileName.endsWith('.pptx')) {
      setTemplateFile(file);
      console.log("Template file saved: ", file.name)
    } else {
      alert("Invalid file type. Please upload a .pptx file.")
      e.target.value = "";
    }
  }

  function handleKeyFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    const fileName = file.name.toLowerCase();
    if (fileName.endsWith('.ppttc') || fileName.endsWith('.csv')) {
      setKeyFile(file);
      console.log("Key file saved: ", file.name);
    } else {
      alert("Invalid file type. Please upload a .ppttc or .csv file.");
      e.target.value = "";
    }
  }

  function handleSubmit(e) {
    e.preventDefault();

    if (uploadSuccess) {
      handleReset();
      return;
    }

    if (isUploading) return;

    setUploadSuccess(false);
    setDownloadURL(null);

    if (!keyFile || !templateFile) {
      alert("Please upload both files before submitting!");
      return;
    }

    console.log("Submitting Key file: ", keyFile.name);
    console.log("Submitting Template file: ", templateFile.name);
    console.log("Required files successfully submitted");

    setIsUploading(true);

    const fastapiURL = import.meta.env.VITE_FASTAPI_ENDPOINT;
    const userID = sessionStorage.getItem('userID');
    const formData = new FormData();

    formData.append('keyFile', keyFile);
    formData.append('templateFile', templateFile)

    fetch(`${fastapiURL}/upload/${userID}/`, {
      method: 'POST',
      body: formData,
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Server Response: ', data);
      const outputURL = `${data.url}?t=${Date.now()}`
      setDownloadURL(outputURL);

      const checkIfFileExists = async (url, retries=10, delay=1000) => {
        for (let i = 0; i < retries; i++) {
          try {
            const response = await fetch(url, { method: 'HEAD' });
            if (response.ok) {
              return true;
            }
          } catch (e) {
            // Retry
          }
          await new Promise(resolve => setTimeout(resolve, delay));
        }
          return false;
        };

        setTimeout(() => {
          checkIfFileExists(outputURL).then(fileAvailable => {
            if (fileAvailable) {
              setUploadSuccess(true);
            } else {
              alert("No output file available. Try Again or contact support.");
            }
            setIsUploading(false);
          });
        }, 15000);
      })
      .catch(error => {
        console.error('Error: ', error);
        setIsUploading(false);
    });
  }

  function handleReset() {
    setKeyFile(null);
    setTemplateFile(null);
    setIsUploading(false);
    setUploadSuccess(false);
    setDownloadURL(null);

    document.getElementById("keyFileInput").value = "";
    document.getElementById("templateFileInput").value="";
  }

  return (
    <>
      <div className="top-text">
        <div className="typing-effect-intro">
          <IntroComponent />
        </div>
        <div className="developed-by">
          <h2 className="h2">
            by <span className="name-highlight">Danny Doan</span>
          </h2>
        </div>
      </div>

      <div className="card">
        <form id="upload-form" onSubmit={handleSubmit}>
          <p className="instructions">Provide proper input files to generate and receive a Thinkcell Powerpoint file:</p>
          <p>1. PPTTC Key</p>
          <input id="keyFileInput" className="choose-file" type="file" name="jsonFile" accept=".ppttc, .csv" onChange={ handleKeyFileChange }/>
          <p>2. PPTX Template</p>
          <input id="templateFileInput" className="choose-file" type="file" name="ppttcFile" accept=".pptx" onChange={ handleTemplateFileChange } />

          <button className="submit-btn" type="submit" disabled={ isUploading }> 
            { isUploading ? 'Processing...': uploadSuccess ? 'Try Another' : 'Submit' 
            } </button>

          <button className="download-btn" type="button" disabled={ !uploadSuccess || !downloadURL } onClick={() => window.open(downloadURL, '_blank')}> {uploadSuccess ? 'Download': 'No Output File' }</button>
        </form>
      </div>
      
      <div className="footer">
        <a className="social-logo" href="https://www.linkedin.com/in/dbdoan/" target="_blank" rel="noreferrer" alt="button to LinkedIn profile">
          <LinkedInIcon />
        </a>

        <a className="social-logo" href="https://github.com/dbdoan/ThinkCellClient" target="_blank" rel="noreferrer" alt="button to Github source code">
          <GithubIcon />
        </a>
      </div>
    </>
  )
}

export default App