import conf from "../conf/conf.js";
import { Client, ID, Databases, Storage, Query } from "appwrite";

export class Service {
  client = new Client();
  databases;
  bucket;

  constructor() {
    this.client
      .setEndpoint(conf.appwriteUrl)
      .setProject(conf.appwriteProjectId);
    this.databases = new Databases(this.client);
    this.bucket = new Storage(this.client);
  }

  // Post methods
  async createPost({ title, slug, content, featuredImage, status, userId }) {
    try {
      return await this.databases.createDocument(
        conf.appwriteDatabaseId,
        conf.appwriteCollectionId,
        slug,
        {
          title,
          content,
          featuredImage,
          status,
          userId,
        }
      );
    } catch (error) {
      console.error("Appwrite service :: createPost :: error", error);
    }
  }

  async updatePost(slug, { title, content, featuredImage, status }) {
    try {
      return await this.databases.updateDocument(
        conf.appwriteDatabaseId,
        conf.appwriteCollectionId,
        slug,
        {
          title,
          content,
          featuredImage,
          status,
        }
      );
    } catch (error) {
      console.error("Appwrite service :: updatePost :: error", error);
    }
  }

  async deletePost(slug) {
    try {
      await this.databases.deleteDocument(
        conf.appwriteDatabaseId,
        conf.appwriteCollectionId,
        slug
      );
      return true;
    } catch (error) {
      console.error("Appwrite service :: deletePost :: error", error);
      return false;
    }
  }

 

  async getPost(slug) {
    try {
      return await this.databases.getDocument(
        conf.appwriteDatabaseId,
        conf.appwriteCollectionId,
        slug
      );
    } catch (error) {
      console.error("Appwrite service :: getPost :: error", error);
      return false;
    }
  }

  async getPosts(queries = [Query.equal("status", "active")]) {
    try {
      return await this.databases.listDocuments(
        conf.appwriteDatabaseId,
        conf.appwriteCollectionId,
        queries
      );
    } catch (error) {
      console.error("Appwrite service :: getPosts :: error", error);
      return false;
    }
  }

  // File upload service
  async uploadFile(file) {
    try {
      return await this.bucket.createFile(
        conf.appwriteBucketId,
        ID.unique(),
        file
      );
    } catch (error) {
      console.error("Appwrite service :: uploadFile :: error", error);
      return false;
    }
  }

  async deleteFile(fileId) {
    try {
      await this.bucket.deleteFile(conf.appwriteBucketId, fileId);
      return true;
    } catch (error) {
      console.error("Appwrite service :: deleteFile :: error", error);
      return false;
    }
  }

  getFilePreview(fileId) {
    return `${this.client.config.endpoint}/storage/buckets/${conf.appwriteBucketId}/files/${fileId}/view?project=${conf.appwriteProjectId}&mode=admin`;
  }

  // Profile methods
  async createProfile({
    developerToken,
    refreshToken,
    clientId,
    clientSecret,
    customerId,
    loginCustomerId,
    youtubeAPIKey,
    InstagramAPIKey,
    image,
    userId,
  }) {
    try {
      return await this.databases.createDocument(
        conf.appwriteDatabaseId,
        conf.appwriteProfileCollectionId,
        ID.unique(),
        {
          developerToken,
          refreshToken,
          clientId,
          clientSecret,
          customerId,
          loginCustomerId,
          youtubeAPIKey,
          InstagramAPIKey,
          image,
          userId,
        }
      );
    } catch (error) {
      console.error("Appwrite service :: createProfile :: error", error);
      return false;
    }
  }

  async updateProfile(userId, updates) {
    try {
      const profile = await this.databases.listDocuments(
        conf.appwriteDatabaseId,
        conf.appwriteProfileCollectionId,
        [Query.equal("userId", userId)]
      );

      if (profile.documents.length > 0) {
        const profileId = profile.documents[0].$id;
        return await this.databases.updateDocument(
          conf.appwriteDatabaseId,
          conf.appwriteProfileCollectionId,
          profileId,
          updates
        );
      } else {
        console.log("Profile not found for user ID:", userId);
        return false;
      }
    } catch (error) {
      console.error("Appwrite service :: updateProfile :: error", error);
      return false;
    }
  }

  async getProfile(userId) {
    try {
      const profile = await this.databases.listDocuments(
        conf.appwriteDatabaseId,
        conf.appwriteProfileCollectionId,
        [Query.equal("userId", userId)]
      );

      if (profile.documents.length > 0) {
        return profile.documents[0];
      } else {
        console.log("Profile not found for user ID:", userId);
        return null;
      }
    } catch (error) {
      console.error("Appwrite service :: getProfile :: error", error);
      return null;
    }
  }

  async listProfiles() {
    try {
      return await this.databases.listDocuments(
        conf.appwriteDatabaseId,
        conf.appwriteProfileCollectionId
      );
    } catch (error) {
      console.error("Appwrite service :: listProfiles :: error", error);
      return false;
    }
  }

  async createCampaign({
    title,
    description,
    campaignType,
    languages,
    addresses,
    budget,
    userId,
  }) {
    try {
      return await this.databases.createDocument(
        conf.appwriteDatabaseId,
        conf.appwriteCampaignCollectionId,
        ID.unique(),
        {
          title,
          description,
          campaignType,
          languages,
          addresses,
          budget,
          userId,
        }
      );
    } catch (error) {
      console.error("Appwrite service :: createCampaign :: error", error);
      return false;
    }
  }

  async getCampaign(campaignId) {
    try {
      return await this.databases.getDocument(
        conf.appwriteDatabaseId,
        conf.appwriteCampaignCollectionId,
        campaignId
      );
    } catch (error) {
      console.error("Appwrite service :: getCampaign :: error", error);
      return null;
    }
  }

  async getCampaignsByUserId(userId) {
    try {
      const response = await this.databases.listDocuments(
        conf.appwriteDatabaseId,
        conf.appwriteCampaignCollectionId,
        [Query.equal("userId", userId), Query.orderDesc("$createdAt")]
      );

      return response && response.documents ? response.documents : [];
    } catch (error) {
      console.error("Appwrite service :: getCampaignsByUserId :: error", error);
      return [];
    }
  }
}

const service = new Service();
export default service;
