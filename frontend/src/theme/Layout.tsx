import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import { ChatWidget } from '../components/ChatWidget/ChatWidget';

type LayoutProps = {
  children: React.ReactNode;
} & typeof import('@docusaurus/core/lib/client/exports/ThemeContext').ThemeContext;

export default function Layout(props: LayoutProps) {
  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
        <ChatWidget />
      </OriginalLayout>
    </>
  );
}