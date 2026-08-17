import { useState } from 'react'
import './App.css'

function App() {
  const [defClick, setDefClick] = useState(false);
  const [msg, setMsg] = useState("");
  const [translation, setTranslation] = useState("");
  const [analysis, setAnalysis] = useState([]);
  const [words, setWords] = useState([]);
  const [hover_array, setHoverArray] = useState([]);

  const handleClear = () => {
    setMsg("");
    setWords([]);
    setAnalysis([]);
    setTranslation("");
    setHoverArray([]);
  };

  async function getData(){
    console.log("get data started");
    const translationResponse = await fetch("http://127.0.0.1:5000/api/translate", {
      method: "POST",
      headers: {
        "Content-type" : "application/json",
      },
      body: JSON.stringify({text: msg}),
    });
    const translationResult = await translationResponse.json();
    if (!translationResponse.ok) {
      throw new Error(translationResult.error?.message || "Translation failed");
    }
    setTranslation(translationResult.data.translation);

    const wordResponse = await fetch("http://127.0.0.1:5000/api/translate/words", {
      method: "POST",
      headers:  {
        "Content-type" : "application/json",
      },
      body: JSON.stringify({
        text: msg
      }),
    });
    const wordResult = await wordResponse.json();
    if (!wordResponse.ok) {
      throw new Error(
        wordResult.error?.message || "Segment translation failed"
      );
    }
    setWords(wordResult.data.segments);
    setHoverArray(Array(wordResult.data.segments.length).fill(false))

    //console.log(words);
    
  }

  async function unpack() {
    const response = await fetch("http://127.0.0.1:5000/api/analyze/sentence",{
      method: "POST",
      headers:  {
        "Content-type" : "application/json",
      },
      body: JSON.stringify({text: msg}),
    });
    const result = await response.json();
    console.log("Full response:", result);
    console.log("Sentences:", result.data?.sentences);
    if (!response.ok) {
      throw new Error(
        result.error?.message || "Sentence analysis failed"
      );
    }
    setAnalysis(result.data.sentences);
  }

  return (
    <>

    <header className="app-header">
      <h1>EchoWords</h1>
      <p>Translate text and understand how each sentence works.</p>
    </header>

    <div className="outer-div">
      <section className="text-column">
        <h2>Original Text</h2>

        {words.length === 0 ? 
          <div>
            <textarea className="box" placeholder="Enter Text" onChange={(e) => setMsg(e.target.value)} value={msg}>
            </textarea>
          </div>
          : 
          <div className="box box2">
            {words.map((segment, i) => {
              if(segment.type === "whitespace"){
                return (
                  <span key={i}>{segment.source}</span>
                );
              }

              return (
              <span key={i} className="definition">
              {hover_array[i] && (<span className="hover-word">{segment.translation}</span>)}

              <span className="word" style={hover_array[i] ? {"backgroundColor": "yellow"} : {}} 
              onMouseEnter={() => 
                setHoverArray((arr) => [...arr.slice(0, i), true, ...arr.slice(i+1)])} 
              onMouseLeave={() => 
                setHoverArray((arr) => [...arr.slice(0, i), false, ...arr.slice(i+1)])}
              >{segment.source}
              </span>
            </span>)
            }
          )}
          </div>}
      </section>
      
      <section className="text-column">
        <h2>English Translation</h2>
        <div className="box translation-box">
          {translation || (
            <span className="empty-message">Your translation will appear here.</span>
          )}
        </div>
      </section>

    </div>
      <div className="btn-container1">
      <button className="first-btn" disabled={!msg.trim()} onClick={()=>getData()} >Translate</button>
      <button className="first-btn" onClick={handleClear}>Clear</button>
      </div>
      <div className="analysis-section">
        <div className="section-heading">
          <div>
            <h2>Sentence analysis</h2>
            <p>Explore grammar, structure, and sentence components.</p>
          </div>
          <button className="secondary-btn" disabled={!msg.trim()} onClick={unpack}>Analyze</button>
        </div>
        
        <div className="lower-box">
          {analysis.length === 0 ? (
            <span className="empty-message">
              Analyze the text to see a detailed explanation.
            </span>
          ) : (
            analysis.map((sentence, i) => (
            <div key={i} className="analysis-line">
              <div><b>Sentence:</b> {sentence.source}</div>
              <div><b>Translation:</b> {sentence.translation}</div>
              <div><b>Structure:</b> {sentence.structure}</div>
              <div><b>Explanation:</b> {sentence.explanation}</div>
              <div className="components">
                <h3>Components</h3>
                {sentence.components.map((component, componentIndex) => (
                <div key={componentIndex} className="component">
                  <div>
                    <b>Source:</b> {component.source}
                  </div>

                  <div>
                    <b>Translation:</b> {component.translation}
                  </div>

                  <div>
                    <b>Role:</b> {component.role}
                  </div>

                  <div>
                    <b>Part of speech:</b> {component.part_of_speech}
                  </div>
                </div>
              ))}
              </div>
            </div>
          )))}
        </div>  
      </div>
    </>
  )
}

export default App;
