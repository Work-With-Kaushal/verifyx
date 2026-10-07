import { useState } from "react";
import "./styles.css";

const API_URL = "https://verifyx-backend-s31f.onrender.com";

function App() {
    const [showLogin, setShowLogin] = useState(false);
    const [showRegister, setShowRegister] = useState(false);

    return (
        <div className="app">
            <header className="navbar">
                <div className="brand">
                    <div className="brand-icon">✓</div>
                    <div>
                        <h1>Veri-X</h1>
                        <span>"Verify Anywhere--Track Everything--Trust Instantly"</span>
                    </div>
                </div>

                <div className="nav-links">
                    <a href="#home">Home</a>
                    <a href="#features">Features</a>
                    <a href="#workflow">Workflow</a>
                    <a href="#verify">Verify</a>

                    <button
                        className="btn btn-outline"
                        onClick={() => setShowLogin(true)}
                    >
                        Login
                    </button>

                    <button
                        className="btn btn-primary"
                        onClick={() => setShowRegister(true)}
                    >
                        Register
                    </button>
                </div>
            </header>

            <main>
                <section className="hero" id="home">
                    <div className="hero-content">
                        <div className="badge">SIH 2026 • Problem Statement 26036</div>

                        <h2>
                            Online Verification of
                            <span> Weighing & Measuring Instruments</span>
                        </h2>

                        <p>
                            A secure digital platform for registration, inspection,
                            verification, certification and public QR-based validation.
                        </p>

                        <div className="hero-buttons">
                            <button
                                className="btn btn-primary btn-large"
                                onClick={() => setShowRegister(true)}
                            >
                                Get Started →
                            </button>

                            <button className="btn btn-light btn-large">
                                Verify Certificate
                            </button>
                        </div>

                        <div className="stats">
                            <div>
                                <strong>100%</strong>
                                <span>Digital Records</span>
                            </div>

                            <div>
                                <strong>SHA-256</strong>
                                <span>Integrity</span>
                            </div>

                            <div>
                                <strong>QR</strong>
                                <span>Public Verification</span>
                            </div>
                        </div>
                    </div>

                    <div className="hero-card">
                        <div className="card-header">
                            <span>✓</span>
                            <div>
                                <strong>Certificate Verified</strong>
                                <small>Veri-X Digital Certificate</small>
                            </div>
                        </div>

                        <div className="certificate">
                            <p>Certificate ID</p>
                            <h3>VX-26036-2026-001</h3>

                            <div className="certificate-row">
                                <div>
                                    <span>Instrument</span>
                                    <strong>Electronic Weighing Scale</strong>
                                </div>

                                <div>
                                    <span>Status</span>
                                    <strong className="verified">VERIFIED</strong>
                                </div>
                            </div>

                            <div className="hash">
                                <span>Integrity Hash</span>
                                <code>a83f...92bd</code>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="features" id="features">
                    <div className="section-heading">
                        <span>CORE FEATURES</span>
                        <h2>Everything in one platform</h2>
                        <p>
                            A complete digital lifecycle for instrument verification.
                        </p>
                    </div>

                    <div className="feature-grid">
                        <Feature
                            icon="📋"
                            title="Digital Registration"
                            text="Register instruments and submit verification applications online."
                        />

                        <Feature
                            icon="📱"
                            title="QR Verification"
                            text="Verify certificates instantly using a secure QR code."
                        />

                        <Feature
                            icon="🔐"
                            title="Hash Integrity"
                            text="SHA-256 based integrity verification helps detect record changes."
                        />

                        <Feature
                            icon="📍"
                            title="District Visibility"
                            text="Monitor compliance and verification activity district-wise."
                        />

                        <Feature
                            icon="📸"
                            title="Field Inspection"
                            text="Officers can record inspection results and evidence."
                        />

                        <Feature
                            icon="🔄"
                            title="Offline Sync"
                            text="Support field operations with offline-first data synchronization."
                        />
                    </div>
                </section>

                <section className="workflow" id="workflow">
                    <div className="section-heading">
                        <span>VERIFICATION LIFECYCLE</span>
                        <h2>From application to certificate</h2>
                    </div>

                    <div className="workflow-grid">
                        <Step number="01" title="Registration" />
                        <Step number="02" title="Application" />
                        <Step number="03" title="Inspection" />
                        <Step number="04" title="Verification" />
                        <Step number="05" title="Certificate" />
                        <Step number="06" title="QR Validation" />
                    </div>
                </section>

                <section className="verify-section" id="verify">
                    <div>
                        <span>PUBLIC VERIFICATION</span>
                        <h2>Verify a certificate instantly</h2>
                        <p>
                            Enter a Veri-X certificate ID to check its current verification
                            status.
                        </p>
                    </div>

                    <div className="verify-box">
                        <input
                            type="text"
                            placeholder="Enter Certificate ID"
                        />
                        <button className="btn btn-primary">Verify</button>
                    </div>
                </section>
            </main>

            <footer>
                <div>
                    <strong>Veri-X</strong>
                    <p>Secure • Digital • Transparent</p>
                </div>

                <p>SIH Problem Statement 26036</p>
            </footer>

            {showLogin && (
                <Modal title="Login" close={() => setShowLogin(false)}>
                    <input className="modal-input" placeholder="Email" type="email" />
                    <input
                        className="modal-input"
                        placeholder="Password"
                        type="password"
                    />
                    <button className="btn btn-primary full">Login</button>
                </Modal>
            )}

            {showRegister && (
                <Modal title="Create Veri-X Account" close={() => setShowRegister(false)}>
                    <input className="modal-input" placeholder="Full Name" />
                    <input className="modal-input" placeholder="Email" type="email" />
                    <input
                        className="modal-input"
                        placeholder="Password"
                        type="password"
                    />

                    <select className="modal-input">
                        <option value="applicant">Applicant</option>
                        <option value="officer">Officer</option>
                    </select>

                    <button className="btn btn-primary full">
                        Create Account
                    </button>
                </Modal>
            )}
        </div>
    );
}

function Feature({ icon, title, text }) {
    return (
        <div className="feature-card">
            <div className="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
    );
}

function Step({ number, title }) {
    return (
        <div className="step">
            <div className="step-number">{number}</div>
            <h3>{title}</h3>
        </div>
    );
}

function Modal({ title, close, children }) {
    return (
        <div className="modal-overlay" onClick={close}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" onClick={close}>
                    ×
                </button>

                <h2>{title}</h2>

                {children}
            </div>
        </div>
    );
}

export default App;