import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';

type FeatureItem = {
  title: string;
  icon: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Advanced AI Tutoring',
    icon: '🧠',
    description: (
      <>
        Get personalized guidance from our AI tutor specialized in Physical AI and Humanoid Robotics concepts.
      </>
    ),
  },
  {
    title: 'Interactive Learning',
    icon: '🎮',
    description: (
      <>
        Engage with hands-on exercises and simulations that bring robotics concepts to life.
      </>
    ),
  },
  {
    title: 'Cutting-Edge Content',
    icon: '🔬',
    description: (
      <>
        Access the latest research and developments in humanoid robotics and physical AI systems.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className="feature-card glass-card">
      <div className="feature-icon">
        {icon}
      </div>
      <Heading as="h3" className="feature-title">{title}</Heading>
      <p className="feature-description">{description}</p>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className="section">
      <div className="container">
        <Heading as="h2" className="section-title">Learning Features</Heading>
        <div className="features-grid">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
