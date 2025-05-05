export interface NewsItem {
    id: number;
    title: string;
    summary: string;
    content: string;
    source: string;
    url: string;
    image?: string;
    created_at: string;
    processed_at?: string;
  }