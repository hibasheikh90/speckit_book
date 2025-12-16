import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import { ChatProvider } from '../../contexts/ChatContext';
import { ChatWidgetWithProvider } from '../../components/ChatWidget/ChatWidget';

const Layout = (props: any) => {
  return (
    <ChatProvider>
      <OriginalLayout {...props}>
        {props.children}
        <ChatWidgetWithProvider />
      </OriginalLayout>
    </ChatProvider>
  );
};

export default Layout;