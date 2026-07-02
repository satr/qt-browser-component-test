import { useMemo, useState } from 'react'

export default function App() {
  const [count, setCount] = useState(0)
  const legacyHint = useMemo(
    () =>
      typeof window !== 'undefined' &&
      typeof window.Promise !== 'undefined' &&
      typeof Array.from === 'function',
    [],
  )

  return (
    <main className="page">
      <section className="card">
        <p className="eyebrow">React + Vite</p>
        <h1>Legacy bundle test</h1>
        <p>
          This page is meant to load the Vite legacy assets, including
          <code>polyfills-legacy-*.js</code>.
        </p>
        <p className={legacyHint ? 'status ok' : 'status bad'}>
          {legacyHint ? 'Modern APIs available' : 'Missing expected APIs'}
        </p>
        <button type="button" onClick={() => setCount((value) => value + 1)}>
          Clicked {count} times
        </button>
      </section>
    </main>
  )
}
