import React from 'react'
import LiveFeedPlayer from '../components/LiveFeedPlayer'

export default function LiveView() {
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Live Traffic Feed</h1>
      <LiveFeedPlayer />
    </div>
  )
}
