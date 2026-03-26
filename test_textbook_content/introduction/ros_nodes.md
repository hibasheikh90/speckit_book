---
title: ROS 2 Nodes
description: Understanding ROS 2 nodes and their role in robotics
---

# ROS 2 Nodes

## Introduction

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

## What is a Node?

A node is a process that performs computation. Nodes are combined together to form a complete ROS system. Nodes written in different programming languages can be run on different machines connected together in a network. This distributed nature of ROS is one of its key features.

### Key Characteristics of Nodes

- **Communication**: Nodes communicate with each other by passing messages.
- **Topics**: Nodes can publish messages to a topic or subscribe to a topic to receive messages.
- **Services**: Nodes can provide services or call services provided by other nodes.
- **Parameters**: Nodes can store and access parameters from a central parameter server.

## Creating a Node

To create a basic node in Python, you would typically:

1. Initialize the ROS client library
2. Create a node
3. Keep the node running until it's interrupted
4. Shutdown the ROS client library

### Example Code

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World'
        self.publisher.publish(msg)
```

## Best Practices

When designing nodes, consider:

- **Modularity**: Keep nodes focused on a single task
- **Communication**: Use appropriate communication patterns (topics, services, actions)
- **Error Handling**: Implement proper error handling and recovery mechanisms
- **Performance**: Optimize for the computational constraints of your robot