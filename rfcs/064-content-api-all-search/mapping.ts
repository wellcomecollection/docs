const mappings = {
  dynamic: "strict",
  properties: {
    id: {
      type: "keyword",
    },
    uid: {
      type: "keyword",
    },
    display: {
      type: "object",
      enabled: false,
    },
    query: {
      properties: {
        type: {
          type: "text",
          shingles: {
            type: "text",
            analyzer: "english_shingle_analyzer",
          },
          cased: {
            type: "text",
            analyzer: "english_cased_analyzer",
          },
          keyword: {
            type: "keyword",
            normalizer: "keyword_lowercase",
          },
        },
        title: {
          type: "text",
          fields: {
            shingles: {
              type: "text",
              analyzer: "english_shingle_analyzer",
            },
            cased: {
              type: "text",
              analyzer: "english_cased_analyzer",
            },
            keyword: {
              type: "keyword",
              normalizer: "keyword_lowercase",
            },
          },
        },
        contributors: {
          type: "text",
          fields: {
            shingles: {
              type: "text",
              analyzer: "english_shingle_analyzer",
            },
            keyword: {
              type: "keyword",
              normalizer: "keyword_lowercase",
            },
          },
        },
        description: {
          type: "text",
          fields: {
            shingles: {
              type: "text",
              analyzer: "english_shingle_analyzer",
            },
            cased: {
              type: "text",
              analyzer: "english_cased_analyzer",
            },
          },
        },
        body: {
          type: "text",
          fields: {
            shingles: {
              type: "text",
              analyzer: "english_shingle_analyzer",
            },
            cased: {
              type: "text",
              analyzer: "english_cased_analyzer",
            },
          },
        },
      },
    },
  },
};

type QueryMapping = {
  type: string;
  title: string;
  description: string;
  body?: string; // Visual story will not have body queriable
  contributors?: string[]; // Not all types have relevant contributors
};

export type DocumentMapping = {
  id: string;
  uid: string;
  display: any;
  query: QueryMapping;
};
