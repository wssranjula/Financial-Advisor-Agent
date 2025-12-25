
import { Suspense } from 'react'
import AuthCallbackClient from './AuthCallbackClient'

export default function AuthCallback() {
  return (
    <Suspense>
      <AuthCallbackClient />
    </Suspense>
  )
}
