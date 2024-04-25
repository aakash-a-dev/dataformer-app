module.exports = {
  docs: [
    {
      type: "category",
      label: " Getting Started",
      collapsed: false,
      items: [
        "index",
        "getting-started/cli",
        // "guides/basic-prompting",
        // "guides/document-qa",
        // "guides/blog-writer",
        // "guides/memory-chatbot",
        "guides/rag-with-astradb",
      ],
    },
    {
      type: "category",
      label: " What's New",
      collapsed: false,
      items: [
        "whats-new/a-new-chapter-langflow",
        "whats-new/migrating-to-one-point-zero",
      ],
    },

    {
      type: "category",
      label: " Migration Guides",
      collapsed: false,
      items: [
        "migration/possible-installation-issues",
        // "migration/flow-of-data",
        "migration/inputs-and-outputs",
        // "migration/supported-frameworks",
        // "migration/sidebar-and-interaction-panel",
        // "migration/new-categories-and-components",
        "migration/text-and-record",
        // "migration/custom-component",
        "migration/compatibility",
        // "migration/multiple-flows",
        // "migration/component-status-and-data-passing",
        // "migration/connecting-output-components",
        // "migration/renaming-and-editing-components",
        // "migration/passing-tweaks-and-inputs",
        "migration/global-variables",
        // "migration/experimental-components",
        // "migration/state-management",
      ],
    },
    {
      type: "category",
      label: "Guidelines",
      collapsed: false,
      items: [
        "guidelines/login",
        "guidelines/api",
        "guidelines/components",
        // "guidelines/features",
        "guidelines/collection",
        "guidelines/prompt-customization",
        // "guidelines/chat-interface",
        // "guidelines/chat-widget",
        // "guidelines/custom-component",
      ],
    },
    {
      type: "category",
      label: "Extended Components",
      collapsed: false,
      items: ["guides/langfuse_integration"],
    },
    {
      type: "category",
      label: "Core Components",
      collapsed: false,
      items: [
        "components/inputs",
        "components/outputs",
        "components/data",
        "components/models",
        "components/helpers",
        "components/vector-stores",
        "components/embeddings",
      ],
    },
    {
      type: "category",
      label: "Extended Components",
      collapsed: false,
      items: [
        "components/agents",
        "components/chains",
        "components/loaders",
        "components/experimental",
        "components/utilities",
        "components/memories",
        "components/model_specs",
        "components/retrievers",
        "components/text-splitters",
        "components/toolkits",
        "components/tools",
      ],
    },
    // {
    //   type: "category",
    //   label: "Examples",
    //   collapsed: false,
    //   items: [
    //     // "examples/flow-runner",
    //     // "examples/conversation-chain",
    //     // "examples/buffer-memory",
    //     // "examples/csv-loader",
    //     // "examples/searchapi-tool",
    //     // "examples/serp-api-tool",
    //     // "examples/python-function",
    //   ],
    // },
    {
      type: "category",
      label: "Deployment",
      collapsed: false,
      items: ["deployment/gcp-deployment"],
    },
    {
      type: "category",
      label: "Contributing",
      collapsed: false,
      items: [
        "contributing/how-contribute",
        "contributing/github-issues",
        "contributing/community",
      ],
    },
  ],
};