import { useEffect, useRef, useState } from 'react'

import Navbar from './components/Navbar'
import StatsCard from './components/StatsCard'
import EventLog from './components/EventLog'

export default function App() {

  const videoRef = useRef(null)

  const canvasRef = useRef(null)

  const sendingRef = useRef(false)

  const [threats, setThreats] = useState([])

  useEffect(() => {

    const interval = setInterval(async () => {

      try {

        const response = await fetch(
          'http://127.0.0.1:8000/threats'
        )

        const data = await response.json()

        setThreats(data)

      } catch (err) {

        console.log(err)

      }

    }, 1000)

    return () => clearInterval(interval)

  }, [])

  const startSharing = async () => {

    const stream =
      await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: false
      })

    videoRef.current.srcObject = stream

    await videoRef.current.play()

    const canvas = canvasRef.current

    const ctx = canvas.getContext('2d')

    canvas.width = 1280
    canvas.height = 720

    const sendFrames = async () => {

      if (
        !videoRef.current ||
        videoRef.current.readyState !== 4
      ) {

        requestAnimationFrame(sendFrames)
        return

      }

      if (sendingRef.current) {

        requestAnimationFrame(sendFrames)
        return

      }

      sendingRef.current = true

      ctx.drawImage(
        videoRef.current,
        0,
        0,
        1280,
        720
      )

      canvas.toBlob(async (blob) => {

        try {

          const formData = new FormData()

          formData.append(
            'file',
            blob,
            'frame.jpg'
          )

          await fetch(
            'http://127.0.0.1:8000/upload_frame',
            {
              method: 'POST',
              body: formData
            }
          )

        } catch (err) {

          console.log(err)

        }

        sendingRef.current = false

        requestAnimationFrame(sendFrames)

      }, 'image/jpeg', 0.7)

    }

    sendFrames()

  }

  return (

    <div
      style={{
        minHeight: '100vh',
        background: '#020817',
        padding: '16px',
        color: 'white',
        fontFamily: 'Arial'
      }}
    >

      <Navbar />

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: '16px',
          marginTop: '16px'
        }}
      >

        <StatsCard
          title='SYSTEM STATUS'
          value='ACTIVE'
        />

        <StatsCard
          title='TRACKING'
          value='LIVE'
        />

        <StatsCard
          title='STREAM'
          value='CONNECTED'
        />

      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '2fr 1fr',
          gap: '16px',
          marginTop: '16px'
        }}
      >

        <div
          style={{
            background: '#061226',
            border: '1px solid #13233d',
            borderRadius: '22px',
            padding: '18px'
          }}
        >

          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >

            <div>

              <h2
                style={{
                  color: '#67e8f9',
                  margin: 0
                }}
              >
                Live Surveillance Feed
              </h2>

              <p
                style={{
                  color: '#64748b',
                  marginTop: '8px'
                }}
              >
                AI-powered object detection & tracking
              </p>

            </div>

            <button
              onClick={startSharing}
              style={{
                background: '#38bdf8',
                border: 'none',
                color: 'white',
                padding: '14px 22px',
                borderRadius: '14px',
                fontWeight: 'bold',
                cursor: 'pointer'
              }}
            >
              Share Screen
            </button>

          </div>

          <div
            style={{
              marginTop: '16px',
              borderRadius: '18px',
              overflow: 'hidden',
              border: '2px solid #13233d',
              background: 'black'
            }}
          >

            <img
              src="http://127.0.0.1:8000/video_feed"
              alt="feed"
              style={{
                width: '100%',
                height: '650px',
                objectFit: 'contain'
              }}
            />

          </div>

        </div>

        <EventLog logs={threats} />

      </div>

      <video
        ref={videoRef}
        style={{
          display: 'none'
        }}
      />

      <canvas
        ref={canvasRef}
        style={{
          display: 'none'
        }}
      />

    </div>

  )

}
