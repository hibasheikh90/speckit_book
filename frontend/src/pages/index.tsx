import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <section className="hero-section">
      <div className="hero-content">
        <div className="hero-text">
          <h1 className="hero-title">
            Physical AI & Humanoid Robotics
          </h1>
          <p className="hero-subtitle">Master the future of AI-powered robotics with hands-on learning</p>
          <Link className="hero-cta" to="/docs/intro">
            Sign in to Read
          </Link>
        </div>
        <div className="hero-robot">
          <div className="robot-container">
            <div className="spotlight"></div>
            <div className="robot-frame">
              <div className="robot-icon">🤖</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
