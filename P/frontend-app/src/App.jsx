import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import About from './pages/About';
import Features from './pages/Features';
import Predict from './pages/Predict';
import Contact from './pages/Contact';

const NotFound = () => (
  <div className="container flex flex-col items-center justify-center min-h-[60vh] text-center">
    <h1 className="text-4xl font-bold mb-4">404</h1>
    <p className="text-muted-foreground mb-8">Page not found</p>
    <a href="/" className="text-primary hover:underline">Return Home</a>
  </div>
);

function App() {
  return (
    <div className="relative flex min-h-screen flex-col bg-background font-sans antialiased">
      <div className="absolute inset-0 bg-grid-pattern pointer-events-none -z-10" />
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/features" element={<Features />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
