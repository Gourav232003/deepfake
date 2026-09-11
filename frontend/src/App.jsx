import { Routes, Route, Link } from "react-router-dom";
import Landing from "./pages/Landing.jsx";
import DetectPage from "./pages/DetectPage.jsx";
import AuthenticatePage from "./pages/AuthenticatePage.jsx";
import VerifyPage from "./pages/VerifyPage.jsx";

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-graphite-100">
        <div className="mx-auto flex max-w-content items-center justify-between px-6 py-4">
          <Link to="/" className="font-semibold text-graphite-900">
            DeepGuard
          </Link>
          <nav className="flex gap-6 text-sm text-graphite-500">
            <Link to="/detect/image">Detect</Link>
            <Link to="/authenticate">Authenticate</Link>
            <Link to="/verify">Verify</Link>
          </nav>
        </div>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/detect/:mediaType" element={<DetectPage />} />
          <Route path="/authenticate" element={<AuthenticatePage />} />
          <Route path="/verify" element={<VerifyPage />} />
        </Routes>
      </main>
    </div>
  );
}
