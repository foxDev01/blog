<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-semibold text-gray-900 mb-2">Мои статьи</h1>
          <p class="text-sm text-gray-600">
            Управляйте своими публикациями
          </p>
        </div>
        
        <router-link
          to="/posts/create"
          class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Создать статью
        </router-link>
      </div>

      <!-- Информация о подписке -->
      <div class="bg-white rounded-md shadow-sm border border-gray-200 p-4 mb-8">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <!-- Существующие фильтры -->
            <select
              v-model="statusFilter"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
            >
              <option value="">Все статьи</option>
              <option value="published">Опубликованные</option>
              <option value="draft">Черновики</option>
            </select>
            
            <select
              v-model="categoryFilter"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
            >
              <option value="">Все категории</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            
            <button
              @click="applyFilters"
              class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
            >
              Применить
            </button>
          </div>
          
        
      
        </div>
      </div>

      <!-- Список постов -->
      <div v-if="postsStore.isLoading" class="space-y-4">
        <PostCardSkeleton v-for="i in 5" :key="i" />
      </div>

      <div v-else-if="myPosts.length > 0" class="space-y-4">
        <div
          v-for="post in myPosts"
          :key="post.id"
          class="bg-white rounded-md shadow-sm border border-gray-200 p-6"
        >
          <div class="flex items-start justify-between">
            <!-- Информация о посте -->
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-2">
                <router-link
                  :to="{ name: 'PostDetail', params: { slug: post.slug } }"
                  class="text-lg font-medium text-gray-900 hover:text-blue-600 transition-colors"
                >
                  {{ post.title }}
                </router-link>
                
                <!-- Статусы -->
                <div class="flex items-center space-x-2">
                  <span
                    v-if="post.status === 'draft'"
                    class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-50 text-yellow-800"
                  >
                    Черновик
                  </span>
           
                </div>
              </div>
              
              <!-- Краткое содержание -->
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">
                {{ getPostExcerpt(post.content) }}
              </p>
              
              <!-- Метаданные -->
              <div class="flex items-center space-x-4 text-sm text-gray-500">
                <span>{{ formatDate(post.created_at) }}</span>
                <span class="flex items-center space-x-1">
                  <EyeIcon class="w-4 h-4" />
                  <span>{{ post.views_count || 0 }}</span>
                </span>
                <span class="flex items-center space-x-1">
                  <ChatBubbleLeftIcon class="w-4 h-4" />
                  <span>{{ post.comments_count || 0 }}</span>
                </span>
                <span v-if="post.category" class="text-blue-600">
                  {{ post.category }}
                </span>
              </div>
            </div>
            
            <!-- Действия -->
            <div class="flex items-center space-x-2 ml-4">
      
              
              <!-- Редактировать -->
              <router-link
                :to="{ name: 'PostEdit', params: { slug: post.slug } }"
                class="p-2 text-gray-400 hover:text-blue-600 rounded-md hover:bg-blue-50 transition-colors"
                title="Редактировать"
              >
                <PencilIcon class="w-5 h-5" />
              </router-link>
              
              <!-- Удалить -->
              <button
                @click="deletePost(post)"
                class="p-2 text-gray-400 hover:text-red-600 rounded-md hover:bg-red-50 transition-colors"
                title="Удалить"
              >
                <TrashIcon class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { usePostsStore } from '@/stores/posts'
import { useAuthStore } from '@/stores/auth'

import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'
import PostListItem from '@/components/posts/PostListItem.vue'
import PostCardSkeleton from '@/components/ui/PostCardSkeleton.vue'
import { 
  PlusIcon, 
  DocumentTextIcon,
  CheckIcon,
  ExclamationTriangleIcon,
  StarIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  ChatBubbleLeftIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'MyPostsView',
  components: { 
    PostListItem, 
    PostCardSkeleton, 
    PlusIcon, 
    DocumentTextIcon,
    CheckIcon,
    ExclamationTriangleIcon,
    StarIcon,
    PencilIcon,
    TrashIcon,
    EyeIcon,
    ChatBubbleLeftIcon
  },
  setup() {
    const postsStore = usePostsStore()
    const authStore = useAuthStore()
  
    const toast = useToast()
    const router = useRouter()
    const statusFilter = ref('')
    const categoryFilter = ref('')
  
    
    const myPosts = computed(() => postsStore.myPosts)
    const categories = computed(() => postsStore.categories)
    
    const applyFilters = async () => {
      const params = {}
      if (statusFilter.value) params.status = statusFilter.value
      if (categoryFilter.value) params.category = categoryFilter.value
      
      await postsStore.fetchMyPosts(params)
    }
    
  
    

    
    const deletePost = async (post) => {
      if (!confirm('Вы уверены, что хотите удалить этот пост?')) {
        return
      }
      
      try {
        await postsStore.deletePost(post.slug)
        toast.success('Пост успешно удален')
        await postsStore.fetchMyPosts()
      } catch (error) {
        console.error('Ошибка удаления поста:', error)
        toast.error('Не удалось удалить пост')
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      })
    }
    
    const getPostExcerpt = (content) => {
      if (!content) return 'Нет содержания'
      return content.length > 150 ? content.substring(0, 150) + '...' : content
    }
    

    
    onMounted(async () => {
      await Promise.all([
        postsStore.fetchMyPosts(),
        postsStore.fetchCategories()
      ])
    })
    
    return {
      postsStore,
      authStore,
    
      myPosts,
      categories,
      statusFilter,
      categoryFilter,
    
      applyFilters,
    
 
      deletePost,
      formatDate,
      getPostExcerpt,
    
    }
  }
}
</script>